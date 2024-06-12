import os
from typing import Optional

from biolib import api, utils
from biolib._internal.file_utils import get_files_and_size_of_directory, get_iterable_zip_stream
from biolib.api import client as api_client
from biolib.biolib_api_client import AppGetResponse, BiolibApiClient
from biolib.biolib_api_client.lfs_types import DataRecordVersion, DataRecordVersionInfo
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger


def push_data_record_version(data_record_uuid: str, input_dir: str, chunk_size_in_mb: Optional[int] = None) -> str:
    BiolibApiClient.assert_is_signed_in(authenticated_action_description='push data to a Data Record')

    if not os.path.isdir(input_dir):
        raise BioLibError(f'Could not find folder at {input_dir}')

    if os.path.realpath(input_dir) == '/':
        raise BioLibError('Pushing your root directory is not possible')

    original_working_dir = os.getcwd()
    os.chdir(input_dir)
    files_to_zip, data_size_in_bytes = get_files_and_size_of_directory(directory=os.getcwd())

    if data_size_in_bytes > 4_500_000_000_000:
        raise BioLibError('Attempted to push directory with a size larger than the limit of 4.5 TB')

    min_chunk_size_bytes = 10_000_000
    chunk_size_in_bytes: int
    if chunk_size_in_mb:
        chunk_size_in_bytes = chunk_size_in_mb * 1_000_000  # Convert megabytes to bytes
        if chunk_size_in_bytes < min_chunk_size_bytes:
            logger.warning('Specified chunk size is too small, using minimum of 10 MB instead.')
            chunk_size_in_bytes = min_chunk_size_bytes
    else:
        # Calculate chunk size based on max chunk count of 10_000, using 9_000 to be on the safe side
        chunk_size_in_bytes = max(min_chunk_size_bytes, int(data_size_in_bytes / 9_000))

    data_size_in_mb = round(data_size_in_bytes / 10**6)
    print(f'Zipping {len(files_to_zip)} files, in total ~{data_size_in_mb}mb of data')

    response = api.client.post(path='/lfs/versions/', data={'resource_uuid': data_record_uuid})
    data_record_version: DataRecordVersion = response.json()
    iterable_zip_stream = get_iterable_zip_stream(files=files_to_zip, chunk_size=chunk_size_in_bytes)

    multipart_uploader = utils.MultiPartUploader(
        use_process_pool=True,
        get_presigned_upload_url_request=dict(
            headers=None,
            requires_biolib_auth=True,
            path=f"/lfs/versions/{data_record_version['uuid']}/presigned_upload_url/",
        ),
        complete_upload_request=dict(
            headers=None,
            requires_biolib_auth=True,
            path=f"/lfs/versions/{data_record_version['uuid']}/complete_upload/",
        ),
    )

    multipart_uploader.upload(payload_iterator=iterable_zip_stream, payload_size_in_bytes=data_size_in_bytes)
    os.chdir(original_working_dir)
    logger.info(f"Successfully pushed a new Data Record version '{data_record_version['uri']}'")
    return data_record_version['uri']


def get_data_record_state_from_uri(uri) -> 'DataRecordVersionInfo':
    app_response: AppGetResponse = api_client.get(path='/app/', params={'uri': uri}).json()
    return DataRecordVersionInfo(
        resource_uri=app_response['app_version']['app_uri'],
        resource_uuid=app_response['app']['public_id'],
        resource_version_uuid=app_response['app_version']['public_id'],
    )
