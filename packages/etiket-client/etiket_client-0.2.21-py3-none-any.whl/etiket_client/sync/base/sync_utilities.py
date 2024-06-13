from etiket_client.local.exceptions import DatasetNotFoundException
from etiket_client.remote.endpoints.dataset import dataset_create, dataset_read, dataset_read_by_alt_uid
from etiket_client.remote.endpoints.file import file_create, file_generate_presigned_upload_link_single, file_read_by_name
from etiket_client.remote.endpoints.models.dataset import DatasetCreate
from etiket_client.remote.endpoints.models.types import FileStatusRem, FileType
from etiket_client.remote.endpoints.models.file import FileCreate

from etiket_client.local.database import Session
from etiket_client.local.dao.dataset import dao_dataset
from etiket_client.local.dao.file import dao_file
from etiket_client.local.models.dataset import  DatasetCreate as DatasetCreateLocal

from etiket_client.sync.base.checksums.hdf5 import md5_netcdf4
from etiket_client.sync.base.checksums.any import md5

from etiket_client.sync.database.dao_sync_items import dao_sync_items
from etiket_client.sync.uploader.file_uploader import upload_new_file_multi, upload_new_file_single
from etiket_client.sync.database.models_pydantic import sync_item, new_sync_item

from etiket_client.python_api.dataset_model.files import generate_version_id

from typing import List, Dict, Optional, Set

import os, json, tempfile, logging, uuid, dataclasses, datetime


logger = logging.getLogger(__name__)

@dataclasses.dataclass
class dataset_info:
    name: str
    datasetUUID: uuid.UUID
    alt_uid: str
    scopeUUID: uuid.UUID
    created: datetime.datetime
    description: Optional[str] = None
    keywords: List[str] = dataclasses.field(default_factory=list)
    attributes: Dict[str, str] = dataclasses.field(default_factory=dict)
    ranking: int = 0
    creator: str = dataclasses.field(default="")

@dataclasses.dataclass
class file_info:
    name : str
    fileName: str

    created: datetime.datetime
    
    fileType : Optional[FileType]
    creator: str = ''
    # TODO standardize this
    file_generator : Optional[str] = None
    
    immutable_on_completion : bool = True # only set to false if you know what you are doing

# TODO proper implementation of immutabilitly of files
class sync_utilities:
    @staticmethod
    def create_ds(live_mode : bool, s_item : sync_item, ds_info : dataset_info):
        try : 
            dataset_read(ds_info.datasetUUID)
        except DatasetNotFoundException:
            try:
                ds = dataset_read_by_alt_uid(ds_info.alt_uid, ds_info.scopeUUID)
                with Session() as session:
                    dao_sync_items.update_uuid(ds_info.datasetUUID, ds.uuid, session)
                s_item.datasetUUID = ds.uuid
                logger.info("Dataset record found on remote server, updated local record.")   
            except DatasetNotFoundException:
                dc = DatasetCreate(uuid = ds_info.datasetUUID, alt_uid= ds_info.alt_uid,
                        collected=ds_info.created,  name = ds_info.name, creator = ds_info.creator,
                        description= ds_info.description, keywords = ds_info.keywords,
                        ranking= ds_info.ranking, scope_uuid = ds_info.scopeUUID, 
                        attributes = ds_info.attributes)
                dataset_create(dc)
                logger.info("Dataset record created on remote server.")    
        
        if live_mode:
            with Session() as session:
                try: 
                    dao_dataset.read(s_item.datasetUUID, session=session)
                except DatasetNotFoundException:
                    dc = DatasetCreateLocal(uuid = s_item.datasetUUID, 
                        alt_uid= ds_info.alt_uid, collected=ds_info.created,
                        name = ds_info.name, creator = ds_info.creator,
                        description= ds_info.description, keywords = ds_info.keywords,
                        ranking= ds_info.ranking, scope_uuid = ds_info.scopeUUID,
                        attributes = ds_info.attributes)
                    dao_dataset.create(dc, session=session)
    
    @staticmethod
    def upload_xarray(xarray_object, s_item : sync_item,  f_info : file_info):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = f'{tmpdirname}/{f_info.name}.h5'
            comp = {"compression": "gzip", "compression_opts": 3}
            encoding = {var: comp for var in list(xarray_object.data_vars)+list(xarray_object.coords)}
            xarray_object.to_netcdf(file_path, engine='h5netcdf', encoding=encoding)
            
            f_info.fileType = FileType.HDF5_NETCDF
            sync_utilities.upload_file(file_path, s_item, f_info)
    
    @staticmethod
    def upload_JSON(content : 'Dict | List | Set | str | int | float', s_item : sync_item, f_info : file_info):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = f'{tmpdirname}/{f_info.name}.json'
            content = json.dumps(content)
            
            f_info.fileType = FileType.JSON
            with open(file_path, 'wb') as file_raw:
                file_raw.write(content.encode())
                file_raw.flush()
            
            sync_utilities.upload_file(file_path, s_item, f_info)
    
    @staticmethod
    def upload_file(file_path, s_item : sync_item, f_info : file_info):
        r_files = []
        try:
            r_files = file_read_by_name(s_item.datasetUUID, f_info.name)    
        except Exception:
            # TODO : check on the type of exception
            logger.info("File %s not found on remote server, creating new file.", f_info.name)
        
        if f_info.fileType is None:
            if file_path.endswith('.h5') or file_path.endswith('.hdf5') or file_path.endswith('.nc'):
                    f_info.fileType = FileType.HDF5_NETCDF
            elif file_path.endswith('.json'):
                f_info.fileType = FileType.JSON
            else:
                f_info.fileType = FileType.UNKNOWN
        
        if f_info.fileType is FileType.HDF5_NETCDF:
            try:
                md5_checksum = md5_netcdf4(file_path)
            except Exception:
                logger.warning("Could not calculate md5 checksum for file %s, of dataset with uuid : %s. This file will be considered as a normal H5 file.", f_info.name, s_item.datasetUUID)
                f_info.fileType = FileType.HDF5
                md5_checksum = md5(file_path)
        else:
            md5_checksum = md5(file_path)
        # TODO fix definition of collected and created on the server
        # create the file entry (if needed)           
        version_id = generate_version_id(f_info.created)
        fc = FileCreate(name = f_info.name, filename=f_info.fileName,
                        creator=f_info.creator, uuid =uuid.uuid4(), collected = f_info.created,
                        size = os.stat(file_path).st_size, type = f_info.fileType,
                        file_generator = f_info.file_generator, version_id = version_id,
                        ds_uuid = s_item.datasetUUID, immutable=f_info.immutable_on_completion)
        
        if len(r_files) == 0:
            try :
                with Session() as session :
                    l_files = dao_file.get_file_by_name(s_item.datasetUUID, f_info.name, session)
                    if len(l_files) > 0:
                        fc.uuid = l_files[0].uuid
            except Exception:
                pass
            
            logger.info("File %s not found on remote server, creating new file.", f_info.name)
            file_create(fc)
        else:
            fc.uuid = r_files[0].uuid
            
            f_dict = {file.version_id : file for file in r_files}
            
            if version_id in f_dict.keys():
                if f_dict[version_id].md5_checksum == md5_checksum:
                    logger.info("File %s already uploaded to remote server (identical checksum), skipping.", f_info.name)
                    return
                elif f_dict[version_id].md5_checksum is None and  f_dict[version_id].status is FileStatusRem.secured:
                    logger.info("File %s already uploaded to remote server (no checksum present), skipping.", f_info.name)
                    return # this means it is a very old upload, and we should not overwrite it
                elif f_dict[version_id].status is FileStatusRem.pending:
                    # TODO : remove upload_id of the current upload and recheck status?
                    logger.info("File %s is pending, reuploading file.", f_info.name)
                    pass
                elif not f_dict[version_id].immutable:
                    logger.info("File %s is mutable, overwriting file.", f_info.name)
                    # it is likely that this is an old upload, reupload the file 
                else : #create a new version (if needed)
                    # if last file has the same checksum, skip
                    if f_dict[max(f_dict.keys())].md5_checksum == md5_checksum:
                        logger.info("File %s already uploaded to remote server, skipping.", f_info.name)
                        return
                    logger.info("Creating new version for file '%s'.", f_info.name)
                    last_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    fc.version_id = generate_version_id(last_mod_time)
                    file_create(fc)
            else:
                logger.info("Creating new version for file %s.", f_info.name)
                file_create(fc)

        # upload the file
        upload_info = file_generate_presigned_upload_link_single(fc.uuid, version_id)                
        # upload_new_file_multi(file_path, upload_info, md5_checksum)
        upload_new_file_single(file_path, upload_info, md5_checksum)

        logger.info("File %s uploaded to remote server.", f_info.name)

