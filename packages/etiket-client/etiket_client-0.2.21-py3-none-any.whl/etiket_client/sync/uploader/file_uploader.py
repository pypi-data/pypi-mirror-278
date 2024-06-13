import logging, os

from etiket_client.remote.endpoints.file import file_validate_upload_multi, file_validate_upload_single
from etiket_client.remote.endpoints.models.file import FileValidate, FileSignedUploadLink, FileSignedUploadLinks
from etiket_client.remote.client import client

from etiket_client.exceptions import uploadFailedException


logger = logging.getLogger(__name__)

def upload_new_file_single(file_raw_name, upload_info : FileSignedUploadLink, md5_checksum):
    timeout = os.stat(file_raw_name).st_size/100_000
    if timeout < 10 :
        timeout = 10

    with open(file_raw_name, 'rb') as file:
        for n_tries in range(3):
            response = client.session.put(upload_info.url, data=file, timeout=timeout)
            success = True
            if response.status_code >= 400:
                logging.warning('Failed to upload a file with name (%s).\nRAW JSON response :: %s', file_raw_name, response.reason)
                success = False
            if n_tries == 2 and success is False:
                raise uploadFailedException('Failed to upload file.')
            if success is True:
                break
    file_validate_upload_single(FileValidate(uuid=upload_info.uuid, version_id=upload_info.version_id, upload_id='', md5_checksum=md5_checksum, etags=[]))

# TODO on the server side, make sure only one client can upload.
def upload_new_file_multi(file_raw_name, upload_info  : FileSignedUploadLinks, md5_checksum, ntries = 0):
    try:
        n_parts = len(upload_info.presigned_urls)
        chunk_size = upload_info.part_size
        etags = []
        with open(file_raw_name, 'rb') as file:
            for i in range(n_parts):
                file.seek(i * chunk_size)
                data = file.read(chunk_size)

                for n_tries in range(3):
                    success, response = upload_chunk(upload_info.presigned_urls[i], data)
                    if n_tries == 2 and success is False:
                        raise uploadFailedException('Failed to upload file.')
                    if success is True:
                        break

                etags.append(str(response.headers['ETag']))
        
        fv = FileValidate(uuid=upload_info.uuid, version_id=upload_info.version_id,
                            upload_id=upload_info.upload_id, md5_checksum=md5_checksum,
                            etags=etags)
        file_validate_upload_multi(fv)

    except Exception as e:
        if ntries < 3:
            logger.warning('Failed to upload file with name %s.\n Error message :: %s, try %s (and trying again).\n', file_raw_name, e, ntries)
            upload_new_file_multi(file_raw_name, upload_info, ntries+1)
        else :
            logger.exception('Failed to upload file with name %s.\n', file_raw_name)
            raise e
    
def upload_chunk(url, data):
    response = client.session.put(url, data=data, timeout=400) # assume that the upload speed is > 100KB/s

    if response.status_code >=400:
        response_json = None
        if response:
            response_json = response.json()
        logging.warning('Failed to upload a chunk to url with hash (%s).\nRAW JSON response :: %s', hash(url), response_json)
        return False, response
    return True, response