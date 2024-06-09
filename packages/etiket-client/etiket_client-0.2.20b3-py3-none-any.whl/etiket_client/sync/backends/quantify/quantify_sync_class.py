from etiket_client.sync.base.sync_source_abstract import SyncSourceAbstract
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item, new_sync_item, FileType

from datetime import datetime, timedelta
import os, pathlib, dataclasses, typing, xarray

@dataclasses.dataclass
class QuantifyConfigData:
    quantify_directory: pathlib.Path
    set_up : str

class QuantifySync(SyncSourceAbstract):
    SyncAgentName = "Quantify"
    ConfigDataClass = QuantifyConfigData
    MapToASingleScope = True
    LiveSyncImplemented = False

    @staticmethod
    def getNewDatasets(configData: QuantifyConfigData, lastIdentifier: str) -> 'typing.List[new_sync_item] | None':
        current_path = ["", ""]
        if lastIdentifier is not None:
            current_path = lastIdentifier.split('/')
        
        try:
            dirs = next(os.walk(configData.quantify_directory))[1]
        except Exception as e:
            raise Exception(f"Could not find quantify directory: {configData.quantify_directory}. Error : {e}")
        newFileDirs = [dir for dir in dirs if current_path[0] <= dir]
        newFileDirs.sort()

        newSyncIdentifiers = []
        for newFileDir in newFileDirs:
            m_dirs = next(os.walk(os.path.join(configData.quantify_directory, newFileDir)))[1]
            if newFileDir == current_path[0]:
                m_dirs = [m_dir for m_dir in m_dirs if current_path[1] < m_dir]
            
            m_dirs.sort()
            newSyncIdentifiers += [new_sync_item(dataIdentifier=f"{newFileDir}/{dir}") for dir in m_dirs]
        
        return newSyncIdentifiers
    
    @staticmethod
    def checkLiveDataset(configData: QuantifyConfigData, syncIdentifier: sync_item):
        # There does not seem to be anything in a dataset to indicate that it has been completed or not :/
        # TODO : check if this is too slow?
        other_datasets = QuantifySync.getNewDatasets(configData, syncIdentifier.dataIdentifier)
        if len(other_datasets) != 0:
            return False
        
        # check the last time the file is modified:
        dir_content = os.listdir(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier))
        m_files = [content for content in dir_content if content.endswith(".hdf5") or content.endswith(".h5")]
        
        if len(m_files) == 0:
            return False

        m_file = max(m_files, key=lambda f: os.path.getmtime(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, f)))
        path = os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, m_file)
        mod_time = pathlib.Path(path).stat().st_mtime
        if datetime.now() - datetime.fromtimestamp(mod_time) < timedelta(minutes=2):
            return True
        return False
    
    @staticmethod
    def syncDatasetNormal(configData: QuantifyConfigData, syncIdentifier: sync_item):
        create_ds_from_quantify(configData, syncIdentifier, False)
        path = os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith("."): # ignore hidden files (e.g. .DS_Store)
                    continue
                common_prefix = pathlib.Path(os.path.commonprefix([path, root]))
                name = os.path.relpath(str(pathlib.Path(os.path.join(root, file)).with_suffix("")),
                                       common_prefix)

                file_name = file
                file_path = os.path.join(root, file)
                
                f_info = file_info(name = name, fileName = file_name,
                    created = datetime.fromtimestamp(pathlib.Path(os.path.join(root, file)).stat().st_mtime),
                    fileType = None, file_generator = "quantify-core")
                sync_utilities.upload_file(file_path, syncIdentifier, f_info)
    
    @staticmethod
    def syncDatasetLive(configData: QuantifyConfigData, syncIdentifier: sync_item):
        create_ds_from_quantify(configData, syncIdentifier, True)
        raise NotImplementedError


def create_ds_from_quantify(configData: QuantifyConfigData, syncIdentifier: sync_item, live : bool):
    tuid = syncIdentifier.dataIdentifier.split('/')[1][:26]
    name = syncIdentifier.dataIdentifier.split('/')[1][27:]
    created = datetime.strptime(tuid[:18], "%Y%m%d-%H%M%S-%f")
    
    # get variable names in the dataset, this is handy for searching!
    keywords = set()
    try:
        xr_ds = xarray.load_dataset(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, "dataset.hdf5"))
        
        for key in xr_ds.keys():
            if 'long_name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['long_name'])
                continue
            if 'name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['name'])

        for key in xr_ds.coords:
            if 'long_name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['long_name'])
                continue
            if 'name' in xr_ds[key].attrs.keys():
                keywords.add(xr_ds[key].attrs['name'])  
    except:
        pass
    
    ds_info = dataset_info(name = name, datasetUUID = syncIdentifier.datasetUUID,
                alt_uid = tuid, scopeUUID = syncIdentifier.scopeUUID,
                created = created, keywords = list(keywords), 
                attributes = {"set-up" : configData.set_up})
    sync_utilities.create_ds(live, syncIdentifier, ds_info)
    