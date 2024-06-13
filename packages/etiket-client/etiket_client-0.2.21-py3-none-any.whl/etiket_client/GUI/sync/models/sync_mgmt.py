from semantic_version import Version

from etiket_client.sync.backends.core_tools.core_tools_config_class import CoreToolsConfigData
from etiket_client.sync.backends.quantify.quantify_sync_class import QuantifyConfigData
from etiket_client.sync.database.dao_sync_sources import dao_sync_sources
from etiket_client.sync.database.models_pydantic import sync_source
from etiket_client.sync.database.types import SyncSourceStatus, SyncSourceTypes
from etiket_client.sync.backends.qcodes.qcodes_config_class import QCoDeSConfigData

from etiket_client.local.database import Session

from PyQt5.QtCore import pyqtSlot, QAbstractListModel, Qt, QUrl

import pathlib, dataclasses, sys


class synchronisation_manager(QAbstractListModel):
    name = Qt.UserRole + 1
    sourceType = Qt.UserRole + 2
    status = Qt.UserRole + 3
    item_remaining = Qt.UserRole + 4
    total_items = Qt.UserRole + 5
    SourceInfo = Qt.UserRole + 6
    LastUpdate = Qt.UserRole + 7
    items_failed = Qt.UserRole + 8
    items_skipped = Qt.UserRole + 9
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = self.__get_data()

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, QModelIndex, role):
        row = QModelIndex.row()
        if role == self.name:
            return self._data[row].name
        if role == self.sourceType:
            return self._data[row].type.name
        if role == self.status:
            return self._data[row].status.name
        if role == self.item_remaining:
            return self._data[row].items_total - self._data[row].items_synchronized - self._data[row].items_failed - self._data[row].items_skipped
        if role == self.total_items:
            return self._data[row].items_total
        if role == self.items_failed:
            return self._data[row].items_failed
        if role == self.items_skipped:
            return self._data[row].items_skipped
        if role == self.SourceInfo:
            if self._data[row].type is SyncSourceTypes.coretools:
                return self._data[row].config_data['dbname']
            elif self._data[row].type is SyncSourceTypes.qcodes:
                return self._data[row].config_data['database_directory']
            elif self._data[row].type is SyncSourceTypes.quantify:
                return self._data[row].config_data['quantify_directory']
            else:
                return None
        if role == self.LastUpdate:
            return self._data[row].last_update.strftime("%d/%m/%Y %H:%M")

    def __get_data(self):
        with Session() as session:
            data_sources = []
            try:
                data_sources = dao_sync_sources.read_sources(session)
            except Exception as e:
                print(f'something went wrong :: {e}')
                
        return data_sources

    def roleNames(self):
        return {
            Qt.UserRole + 1: b'name',
            Qt.UserRole + 2: b'sourceType',
            Qt.UserRole + 3: b'status',
            Qt.UserRole + 4: b'item_remaining',
            Qt.UserRole + 5: b'total_items',
            Qt.UserRole + 6: b'SourceInfo',
            Qt.UserRole + 7: b'LastUpdate',
            Qt.UserRole + 8: b'items_failed',
            Qt.UserRole + 9: b'items_skipped',
        }

    @pyqtSlot()
    def update(self):
        self.reset_data(None)
    
    def reset_data(self, new_data):
        self.beginResetModel()
        self._data = self.__get_data()
        self.endResetModel()
    
    @pyqtSlot(str, str, str, str, result = str)
    def evaluateQCodesData(self, name, set_up, scope_uuid, path):
        errorstring = ""

        for data in self.__get_data():
            if data.name == name:
                errorstring = f"The name '{name}' already exists.\n"

        if not path.endswith(".db"):
            errorstring += f"Please provide a valid SQL file."
        
        if sys.platform == 'win32':
            path = path.replace("file:///", "")
        else:
            path = QUrl(path).path()

        if errorstring == "":
            with Session() as session:
                qcodesConfig = QCoDeSConfigData(database_directory=pathlib.Path(path),
                                                set_up=set_up)
                syncSource = sync_source(name=name,
                                        type=SyncSourceTypes.qcodes,
                                        status=SyncSourceStatus.pending,
                                        config_data=dataclasses.asdict(qcodesConfig), 
                                        default_scope=scope_uuid,
                                        auto_mapping=False)
                dao_sync_sources.add_new_source(syncSource, session)
        return errorstring

    @pyqtSlot(str, str, str, str, result = str)
    def evaluateQuantifyData(self, name, set_up, scope_uuid, path):
        errorstring = ""

        for data in self.__get_data():
            if data.name == name:
                errorstring = f"The name '{name}' already exists.\n"
                
        if errorstring == "":
            with Session() as session:
                quantifyConfig = QuantifyConfigData(quantify_directory=pathlib.Path(QUrl(path).path()),
                                                set_up=set_up)
                syncSource = sync_source(name=name,
                                        type=SyncSourceTypes.quantify,
                                        status=SyncSourceStatus.pending,
                                        config_data=dataclasses.asdict(quantifyConfig), 
                                        default_scope=scope_uuid,
                                        auto_mapping=False)
                dao_sync_sources.add_new_source(syncSource, session)
        return errorstring
    
    @pyqtSlot(str, str, str, str, str, str, result = str)
    def evaluateCoreToolsData(self, name, database, user, password, port, host):
        errorstring = ""
        
        try:
            import core_tools
        except ImportError:
            errorstring = "Please install the core_tools package."
        
        if errorstring == "":
            if Version(core_tools.__version__) < Version("1.4.42"):
                errorstring = "Please update the core_tools package to version 1.4.42 or higher."
        
        if errorstring == "":
            for data in self.__get_data():
                if data.type is SyncSourceTypes.coretools:
                    if data.name == name:
                        errorstring = f"The name '{name}' already exists.\n"
                    if data.config_data['dbname'] == database and data.config_data['host'] == host:
                        errorstring = f"Already added the database '{database}' on the host '{host}'.\n"
        
        if errorstring == "":
            # check if it connects.
            cred = CoreToolsConfigData(dbname=database, user=user, password=password, port=int(port), host=host)
            try :
                import psycopg2
                conn = psycopg2.connect(**dataclasses.asdict(cred))
            except Exception as e:
                errorstring = f"{str(e)}"
                
        if errorstring == "":
            # check if the measurements table exists.
            try :
                cur = conn.cursor()
                stmt = "SELECT EXISTS ( SELECT FROM  pg_tables WHERE schemaname = 'public' AND  tablename  = 'global_measurement_overview');"
                cur.execute(stmt)
                res = cur.fetchone()[0]
                cur.close()
                conn.close()
                if res == False:
                    errorstring = f"Can connect to the database, but cannot find tables used by the core-tools software -.-. Please make sure core-tools is set-up on this database."
            except Exception as e:
                errorstring = f"An unexpected error occured.\n Error : {str(e)}"
        
        if errorstring == "":
            with Session() as session:
                PC = CoreToolsConfigData(dbname=database, user=user, password=password, port=port, host=host)
                syncSource = sync_source(name=name,
                                        type=SyncSourceTypes.coretools,
                                        status=SyncSourceStatus.pending,
                                        config_data=dataclasses.asdict(PC), 
                                        auto_mapping=True, default_scope=None)
                dao_sync_sources.add_new_source(syncSource, session)
            self.reset_data(None)

        return errorstring