from etiket_client.sync.database.models_db import SyncSourcesSQL
from etiket_client.sync.database.types import SyncSourceTypes

from etiket_client.sync.base.sync_source_abstract import SyncSourceAbstract

from etiket_client.sync.backends.quantify.quantify_sync_class import QuantifySync, QuantifyConfigData
from etiket_client.sync.backends.qcodes.qcodes_sync_class import QCoDeSSync, QCoDeSConfigData
from etiket_client.sync.backends.core_tools.core_tools_sync_class import CoreToolsSync, CoreToolsConfigData

import dataclasses, typing, uuid


type_mapping = {SyncSourceTypes.native : None,
                SyncSourceTypes.quantify : QuantifySync,
                SyncSourceTypes.qcodes : QCoDeSSync,
                SyncSourceTypes.coretools : CoreToolsSync}

config_mapping = {SyncSourceTypes.native : dict,
                SyncSourceTypes.quantify : QuantifyConfigData,
                SyncSourceTypes.qcodes : QCoDeSConfigData,
                SyncSourceTypes.coretools : CoreToolsConfigData}

@dataclasses.dataclass  
class SyncSource:
    id : int
    name : str
    type : SyncSourceTypes
    sync_class : typing.Type[SyncSourceAbstract]
    sync_config : typing.Type[dataclasses.dataclass]
    default_scope : typing.Optional[uuid.uuid4]

    @staticmethod
    def init_from_sql(sync_src : SyncSourcesSQL):
        return SyncSource(id = sync_src.id, name = sync_src.name, type = sync_src.type,
                          sync_class = type_mapping[sync_src.type],
                          sync_config = config_mapping[sync_src.type](**sync_src.config_data),
                          default_scope = sync_src.default_scope)
