from etiket_client.sync.database.models_pydantic import sync_source
from etiket_client.sync.database.dao_sync_sources import dao_sync_sources
from etiket_client.sync.database.types import SyncSourceTypes

def start_up(session):
    # create native sync source.
    ss = sync_source(name="native data", type=SyncSourceTypes.native,
                            config_data={}, auto_mapping=True,
                            default_scope=None)
    try:
        dao_sync_sources.read(ss.name, session)
    except:
        dao_sync_sources.add_new_source(ss, session)