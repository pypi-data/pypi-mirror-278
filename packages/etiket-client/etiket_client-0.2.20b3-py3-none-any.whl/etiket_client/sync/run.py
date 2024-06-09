from etiket_client.local.models.file import FileSelect

from etiket_client.local.dao.file import dao_file, dao_file_delete_queue
from etiket_client.local.dao.dataset import dao_dataset
from etiket_client.local.exceptions import DatasetNotFoundException
from etiket_client.remote.endpoints.models.types import FileType
from etiket_client.sync.backends.native.sync_agent import run_native_sync
from etiket_client.sync.backends.sources import SyncSource
from etiket_client.sync.database.dao_sync_items import dao_sync_items
from etiket_client.sync.database.dao_sync_sources import dao_sync_sources,\
    sync_source_update

from etiket_client.sync.database.models_pydantic import sync_item
from etiket_client.sync.database.types import SyncSourceStatus, SyncSourceTypes

from etiket_client.local.database import Session 

import logging, time
from setproctitle import setproctitle

logger = logging.getLogger(__name__)


def sync_loop():
    running = True
    while running == True:
        try:
            with Session() as session:
                run_sync_iter(session)
        except Exception:
            # usually when connection is lost, try again in 10 seconds.
            logger.exception('Sync loop broken, with error ::')
            time.sleep(1)


def run_sync_iter(session):
    n_syncs = 0
    sync_sources_raw = dao_sync_sources.read_sources(session)
    sync_sources = [SyncSource.init_from_sql(source) for source in sync_sources_raw]        
    
    dao_file_delete_queue.clean_files(session)
    
    for sync_source in sync_sources:
        if sync_source.type == SyncSourceTypes.native:
            logger.info("Syncing %s, of type %s", sync_source.name, sync_source.type)
            items_synced = run_native_sync(sync_source, session)
            n_syncs += items_synced
            continue
        else:
            try:
                logger.info("Syncing %s, of type %s", sync_source.name, sync_source.sync_class.SyncAgentName)
                get_new_sync_items(sync_source, session)
                
                s_item = dao_sync_items.read_sync_item(sync_source.id, offset = 0, session=session)
                
                if s_item is not None:
                    liveDS = sync_source.sync_class.checkLiveDataset(sync_source.sync_config, s_item)
                    # this is needed to not get stuck in a loop of live datasets (though not the cleanest way)
                    liveDS_already_tried = check_live_DS_already_tried(s_item, session)
                    if (liveDS and sync_source.sync_class.LiveSyncImplemented is False) or liveDS_already_tried:
                        # assume only one live dataset at a time.
                        s_item = dao_sync_items.read_sync_item(sync_source.id, offset = 1, session=session)
                        liveDS = False
                
                if s_item is None:
                    ssu = sync_source_update(status=SyncSourceStatus.synchronized)
                    dao_sync_sources.update_status(sync_source.id, ssu, session)
                    logger.info("No new items to sync from %s.", sync_source.name)
                    continue


                liveSync_successful = False
                if liveDS is True:
                    try:
                        logger.info("Syncing live dataset, %s from %s.", s_item.dataIdentifier, sync_source.name)
                        sync_source.sync_class.syncDatasetLive(sync_source.sync_config, s_item)
                        liveSync_successful = True
                        logger.info("Synced live dataset, %s from %s.", s_item.dataIdentifier, sync_source.name)
                        # do not mark as successfull -- upload the final version of the files using the normal sync.
                    except Exception:
                        logger.exception("Failed to synchronize %s from %s.", s_item.dataIdentifier, sync_source.name)
                        dao_sync_items.mark_failed_attempt(sync_source.id, s_item.dataIdentifier,session)
                                            
                if liveDS is False or liveSync_successful is True:
                    try:
                        logger.info("Syncing %s from %s.", s_item.dataIdentifier, sync_source.name)
                        sync_source.sync_class.syncDatasetNormal(sync_source.sync_config, s_item)
                        
                        try: # remove any dataset caches:
                            dataset_local = dao_dataset.read(s_item.datasetUUID, session)
                            for file in dataset_local.files:
                                if file.type == FileType.HDF5_CACHE:
                                    fs = FileSelect(uuid=file.uuid, version_id=file.version_id)
                                    dao_file.delete(fs, session)
                        except DatasetNotFoundException:
                            pass
                        except Exception as e:
                            raise e                            
                        
                        n_syncs += 1
                        logger.info("Synced %s from %s.", s_item.dataIdentifier, sync_source.name)

                        dao_sync_items.mark_successful_sync(sync_source.id, s_item.dataIdentifier ,session)
                    except Exception:
                        logger.exception("Failed to synchronize %s from %s.", s_item.dataIdentifier, sync_source.name)
                        dao_sync_items.mark_failed_attempt(sync_source.id, s_item.dataIdentifier,session)   
                
                # update statistics and state of the sync source.
                n_items = dao_sync_items.count_items(sync_source.id, session)
                n_items_failed = dao_sync_items.count_items_failed(sync_source.id, session)
                n_items_synced = dao_sync_items.count_items_synchronized(sync_source.id, session)
                n_items_skipped = dao_sync_items.count_items_not_in_scope(sync_source.id, session)
                
                ssu = sync_source_update(status=SyncSourceStatus.synchronizing, 
                                        items_total = n_items,
                                        items_synchronized = n_items_synced,
                                        items_skipped=n_items_skipped,
                                        items_failed=n_items_failed)
                
                if n_items == n_items_failed+n_items_skipped+n_items_synced:
                    ssu.status=SyncSourceStatus.synchronized
                    logger.info("Sync source %s is now fully synchronized (failed : %s, skipped %s).", sync_source.name, n_items_failed, n_items_skipped)
                dao_sync_sources.update_status(sync_source.id, ssu, session)
            except Exception:
                logger.exception("Failed to sync %s", sync_source.name)
    if n_syncs == 0:
        time.sleep(1)

def get_new_sync_items(sync_source : SyncSource, session):
    last_identifier = dao_sync_items.get_last_identifier(sync_source.id, session)
    new_items = sync_source.sync_class.getNewDatasets(sync_source.sync_config, last_identifier)
    logger.info("Found %s new items in remote location, to add to the list of things to synchronize.", len(new_items))
    dao_sync_items.write_sync_items(sync_source.id, new_items, session)

def check_live_DS_already_tried(s_item : sync_item, session):
    try:
        dataset = dao_dataset.read(s_item.datasetUUID, session)
        for file in dataset.files:
            if file.type == FileType.HDF5_CACHE:
                return True
    except DatasetNotFoundException:
        return False
    return False

if __name__ == '__main__':
    import etiket_client
    from etiket_client.settings.logging import set_up_sync_logger
    
    logger = set_up_sync_logger(etiket_client.__name__)
    
    try: 
        setproctitle('Python qdrive sync')
    except Exception:
        logger.exception("Failed to set process title.")
    
    sync_loop()