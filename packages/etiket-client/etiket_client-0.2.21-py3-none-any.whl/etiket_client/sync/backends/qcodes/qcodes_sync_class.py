import typing, sqlite3, qcodes as qc, os, json
from datetime import datetime

from etiket_client.sync.base.sync_source_abstract import SyncSourceAbstract
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, new_sync_item, FileType
from etiket_client.sync.backends.qcodes.real_time_sync import QCoDeS_live_sync
from etiket_client.sync.backends.qcodes.qcodes_config_class import QCoDeSConfigData

from qcodes.dataset import initialise_database, load_by_id
from qcodes.utils.helpers import NumpyJSONEncoder


class QCoDeSSync(SyncSourceAbstract):
    SyncAgentName = "QCoDeS"
    ConfigDataClass = QCoDeSConfigData
    MapToASingleScope = True
    LiveSyncImplemented = True

    @staticmethod
    def getNewDatasets(configData: QCoDeSConfigData, lastIdentifier: str) -> 'typing.List[new_sync_item] | None':
        qc.config.core.db_location = str(configData.database_directory)
        initialise_database(journal_mode='WAL')
        
        newSyncIdentifiers = []
        with sqlite3.connect(configData.database_directory) as conn:
            if not lastIdentifier:
                lastIdentifier = 0         
            
            get_newer_guid_query = """SELECT run_id FROM runs
                                      WHERE run_id > ? ORDER BY run_id ASC"""
            
            cursor = conn.cursor()
            cursor.execute(get_newer_guid_query, (int(lastIdentifier),))
            rows = cursor.fetchall()
            
            newSyncIdentifiers += [new_sync_item(dataIdentifier=str(row[0])) for row in rows]
        return newSyncIdentifiers
    
    @staticmethod
    def checkLiveDataset(configData: QCoDeSConfigData, syncIdentifier: sync_item):
        # assume only one measurement happens at a time.
        with sqlite3.connect(configData.database_directory) as conn:
            res = conn.execute("SELECT MAX(run_id) FROM runs")
            max_id = res.fetchone()[0]
        
        if int(syncIdentifier.dataIdentifier) < max_id:
            return False
            
        ds_qc = load_by_id(int(syncIdentifier.dataIdentifier))
        return not ds_qc.completed
    
    @staticmethod
    def syncDatasetNormal(configData: QCoDeSConfigData, syncIdentifier: sync_item):
        ds_qc = create_ds_from_qcodes(configData, syncIdentifier, False)
        ds_xr = ds_qc.to_xarray_dataset()
        
        created_time = datetime.fromtimestamp(ds_qc.run_timestamp_raw)
        if ds_qc.snapshot:
            ds_xr.attrs['snapshot'] = json.dumps(ds_qc.snapshot, cls=NumpyJSONEncoder)
            
            f_info = file_info(name = 'Snapshot', fileName = 'snapshot.json',
                               fileType= FileType.JSON,
                               created = created_time, file_generator = "QCoDeS")
            sync_utilities.upload_JSON(ds_qc.snapshot, syncIdentifier, f_info)
        
        f_info = file_info(name = 'measurement', fileName = 'measured_data.hdf5',
                           fileType= FileType.HDF5_NETCDF,
                           created = created_time, file_generator = "QCoDeS")
        sync_utilities.upload_xarray(ds_xr, syncIdentifier, f_info)

    @staticmethod
    def syncDatasetLive(configData: QCoDeSConfigData, syncIdentifier: sync_item):
        ds_qc = create_ds_from_qcodes(configData, syncIdentifier, True)
        if ds_qc.snapshot:
            created_time = datetime.fromtimestamp(ds_qc.run_timestamp_raw)
            f_info = file_info(name = 'Snapshot', fileName = 'snapshot.json',
                               fileType= FileType.JSON,
                               created = created_time, file_generator = "QCoDeS")
            sync_utilities.upload_JSON(ds_qc.snapshot, syncIdentifier, f_info)
            
        QCoDeS_live_sync(int(syncIdentifier.dataIdentifier), str(configData.database_directory), syncIdentifier.datasetUUID)

def create_ds_from_qcodes(configData: QCoDeSConfigData, syncIdentifier: sync_item, live : bool):
    ds_qc = load_by_id(int(syncIdentifier.dataIdentifier))

    collected_time = datetime.fromtimestamp(ds_qc.run_timestamp_raw)
    
    ranking = 0
    if 'inspectr_tag' in ds_qc.metadata.keys():
        if ds_qc.metadata['inspectr_tag']=='star': ranking=1
        if ds_qc.metadata['inspectr_tag']=='cross': ranking=-1
        
    # get variable names in the dataset, this is handy for searching!
    ds_xr = ds_qc.to_xarray_dataset()
    keywords = set()
    try:        
        for key in ds_xr.keys():
            if 'long_name' in ds_xr[key].attrs.keys():
                keywords.add(ds_xr[key].attrs['long_name'])
                continue
            if 'name' in ds_xr[key].attrs.keys():
                keywords.add(ds_xr[key].attrs['name'])

        for key in ds_xr.coords:
            if 'long_name' in ds_xr[key].attrs.keys():
                keywords.add(ds_xr[key].attrs['long_name'])
                continue
            if 'name' in ds_xr[key].attrs.keys():
                keywords.add(ds_xr[key].attrs['name'])  
    except Exception:
        pass
    
    description = f"database : {os.path.basename(configData.database_directory)} | run ID : {ds_qc.run_id} | GUID : {ds_qc.guid}"
    
    ds_info = dataset_info(name = ds_qc.name, datasetUUID = syncIdentifier.datasetUUID,
                alt_uid = ds_qc.guid, scopeUUID = syncIdentifier.scopeUUID,
                created = collected_time, keywords = list(keywords),  description = description,
                ranking=ranking,
                attributes = {"sample" : ds_qc.sample_name,
                              "experiment name" : ds_qc.exp_name,
                              "set-up" : configData.set_up})
    sync_utilities.create_ds(live, syncIdentifier, ds_info)
    return ds_qc
    