import time
import json
import os
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List, Optional
from urllib.parse import urljoin
from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoderMonitor
from pathlib import Path

from .common import common
from .common import get_uuid
from .common import decode_base64_array
from .common.https_agent import HttpsAgent
from .typing import StudyUnit
from .typing import Species
from .typing import StudyType
from .typing import ChunkSize


class Connector(object):
  """
  Shared functions of all platforms
  """

  def __init__(self, host: str, token: str, ssl: bool = True):
    """
    Parameters
    ----------
    host : str
      The URL of the host server, only support HTTPS connection\n
      Example:
        BBrowserX: https://talk2data.bioturing.com/t2d_index_tool/ \n
        Lens_SC: https://talk2data.bioturing.com/lens_sc/ \n
        Lens_Bulk: https://talk2data.bioturing.com/lens_bulk/ \n
    token : str
      The API token to verify authority. Generated in-app.
    """
    self.__host = host
    self.__token = token
    self.__ssl = ssl
    self.__https_agent = HttpsAgent(self.__token, self.__ssl)


  def _get_error_message(self, response):
    message = None
    if not response:
      message = 'Connection failed'
    elif 'status' not in response or response['status'] != 200:
      if 'traceback' in response:
        message = f"Request fail with traceback:\n{response['traceback']}"
      else:
        message = response.get(
          'detail', 'Internal server error. Please check server log.')
        message = f"Request fail with message:\n{message}"
    elif 'data' in response and 'status' in response['data'] and \
    response['data']['status'] == 'ERROR':
      message = response['data']['log']
      message = f"Request fail with message:\n{message}"
    return message


  def _add_file_upload(self, folder_id, n_chunks, file_name):
    params = {
      'folder_id': folder_id,
      'n_chunks': n_chunks,
      'original_file_name': file_name
    }
    response = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/add_file_upload'),
      body=params
    )

    common.check_result_status(response)
    id = response['data'][0]['id']
    return id


  def _upload_each_file_in_chunk(
      self,
      folder_id,
      id,
      file_path,
      file_name,
      chunk_size,
      n_chunks
    ):
    file = open(file_path, 'rb')
    for chunk_order in range(n_chunks):
      chunk = file.read(chunk_size)

      if not chunk:
        raise Exception('Something went wrong')

      with tqdm(
        desc='{} - chunk_{}'.format(file_name, chunk_order),
        total=chunk_size,
        unit='MB',
        unit_scale=True,
        unit_divisor=1024,
      ) as bar:
        fields = {
          'params': json.dumps({
            'folder_id': folder_id,
            'id': id,
            'chunk': chunk_order,
            'n_chunks': n_chunks,
          }),
          'file': (file_name, chunk)
        }

        encoder = MultipartEncoder(fields=fields)
        multipart = MultipartEncoderMonitor(
          encoder, lambda monitor: bar.update(monitor.bytes_read - bar.n)
        )
        headers = {
          'Content-Type': multipart.content_type,
          'bioturing-api-token': self.__token
        }
        response = requests.post(
          urljoin(self.__host, 'api/v1/upload_chunk'),
          headers=headers,
          data=multipart,
          verify=self.__ssl
        ).json()
        if not response:
          raise Exception('Something went wrong')
        if 'status' not in response or response['status'] != 200:
          raise Exception(response)

    output_dir = response['data']['output_dir']
    return output_dir


  def upload_chunk(self, file_names, files, chunk_size, folder_id: Optional[str] = None):
    """
    :meta private:
    """
    if folder_id is None:
      folder_id = get_uuid()
    for file_name, file in zip(file_names, files):
      file_size = file.stat().st_size
      n_chunks = int(np.ceil(file_size / chunk_size))
      id = self._add_file_upload(
        folder_id,
        n_chunks,
        file_name,
      )
      output_dir = self._upload_each_file_in_chunk(
        folder_id,
        id,
        file,
        file_name,
        chunk_size,
        n_chunks
      )
    return output_dir


  def upload_folder(self, folder, chunk_size):
    REQUIRED_FILES = [
      'coords.npy', 'embeddings.db',
      'matrix.hdf5', 'metadata.db'
    ]
    print(f"Only upload files: {REQUIRED_FILES} and folder: custom_embeddings")

    if not os.path.exists(folder) or not os.path.isdir(folder):
      raise NotADirectoryError(f"Folder {folder} not found")

    folder_id = get_uuid()

    other_files = []
    other_file_names = []

    files_list = os.listdir(folder)
    for f in REQUIRED_FILES:
      if f not in files_list:
        raise FileNotFoundError(f"Cannot find files: {f}")
      other_files.append(Path(os.path.join(folder, f)))
      other_file_names.append(f)

    embedding_dir = os.path.join(folder, 'custom_embeddings')
    if not os.path.exists(embedding_dir) or not os.path.isdir(embedding_dir):
      raise NotADirectoryError("Cannot find custom_embeddings directory")

    embedding_files = []
    embedding_file_names = []
    for f in os.scandir(embedding_dir):
      if os.path.isfile(f.path) and os.path.splitext(f)[1] == '.npy':
        embedding_files.append(Path(f.path))
        embedding_file_names.append(f.name)

    if len(embedding_files) == 0:
      raise FileNotFoundError("Cannot find any file in custom_embeddings")

    res = self.upload_chunk(
      other_file_names, other_files, chunk_size, folder_id=folder_id
    )
    embedding_id = os.path.join(folder_id, 'custom_embeddings')
    self.upload_chunk(
      embedding_file_names, embedding_files, chunk_size, folder_id=embedding_id
    )
    return res


  def post_request(self, api_route, data={}, check_error=True):
    """
    :meta private:
    """
    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, api_route),
      body=data,
      check_error=check_error
    )
    return submission_status


  def test_connection(self):
    """
    Test the connection to the host

    Returns
    ----------
    connection status : str
    """
    url = urljoin(self.__host, 'api/v1/test_connection')
    print(f'Connecting to host at {url}')
    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      print('Connection successful')
      return True
    else:
      print('Connection failed')
    return False


  def get_submission_log(self, group_id: str, task_id: str):
    """
    :meta private:
    """
    last_status = []
    while True:
      submission_log = self.post_request(
        api_route='api/v1/get_submission_log',
        data={'task_id': task_id},
        check_error=False
      )
      message = self._get_error_message(submission_log)
      if message:
        print(message)
        break

      current_status = submission_log['data']['log'].split('\n')[:-1]
      new_status = current_status[len(last_status):]
      if len(new_status):
        print('\n'.join(new_status))

      last_status += new_status
      if submission_log['data']['status'] != 'SUCCESS':
        time.sleep(5)
        continue
      else:
        res = self.post_request(
          api_route='api/v1/commit_submission_result',
          data={
            'group_id': group_id,
            'task_id': task_id
          },
          check_error=False
        )
        message = self._get_error_message(res)
        if message:
          print(message)
          break
        else:
          print('Study submitted successfully!')
          return {
            'status': True,
            'study_info': res['study_info']
          }
    return False


  def get_user_groups(self):
    """
    Get all available groups of current token

    Returns
    ----------
    List of groups' info : List[dict]
      In which:
        'group_id': uuid of the group, which will be used in further steps,\n
        'group_name': displaying name of the group
    """
    res = self.post_request(
      api_route='api/v1/get_user_groups'
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_user_s3(self):
    """
    Get all available groups of current token

    Returns
    ----------
    List of s3 bucket' info : List[dict]
      In which:
        'id': uuid of the s3 bucket, which will be used in further steps,\n
        'bucket': bucket of s3,\n
        'prefix': prefix of s3,\n
      ( s3_path = s3://[bucket]/[prefix]/ )
    """
    res = self.post_request(
      api_route='api/v1/get_user_s3'
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_shared_s3_of_group(self, group_id: str):
    """
    Get all available groups of current token

    Parameters
    ----------
    group_id : str,
      Group hash id (uuid)

    Returns
    ----------
    List of s3 bucket' info : List[dict]
      In which:
        'id': uuid of the s3 bucket, which will be used in further steps,\n
        'bucket': bucket of s3,\n
        'prefix': prefix of s3,\n
      ( s3_path = s3://[bucket]/[prefix]/ )
    """
    res = self.post_request(
      api_route='api/v1/get_shared_s3_of_group',
      data = {
        'group_id': group_id
      }
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_all_studies_info_in_group(
    self,
    species: str,
    group_id: str
  ):
    """
    Get info of all studies within group.

    Parameters
    -------------
    species : bioturing_connector.typing.Species.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id : str,
          Group hash id (uuid)

    Returns
    -------------
    List of studies' info : List[dict]
      In which:
        'uuid': the uuid of study, which will be used in further steps, \n
        'study_hash_id': the displaying id of study on platform,\n
        'created_by': email of person who submitted the study,\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_all_studies_info_in_group',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def query_genes(
    self,
    species: str,
    study_id: str,
    gene_names: List[str],
    unit: str = StudyUnit.UNIT_RAW.value
  ):
    """
    Query genes expression of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    gene_names : List[str]
          Querying gene names. \n
          If gene_names=[], full matrix will be returned
    unit : bioturing_connector.typing.StudyUnit. Default 'raw'
          Expression unit\n
          Support:
            bioturing_connector.typing.StudyUnit.UNIT_LOGNORM.value\n
            bioturing_connector.typing.StudyUnit.UNIT_RAW.value\n

    Returns
    ----------
    expression_matrix : csc_matrix
          Expression matrix, shape=(n_cells, n_genes)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'gene_names': gene_names,
      'unit': unit
    }
    result = self.post_request(
      api_route='api/v1/study/query_genes',
      data=data
    )
    return common.parse_query_genes_result(result)


  def get_metadata_fields(
    self,
    species: str,
    study_id: str,
    group_id: str = None,
  ):
    """
    Get full metadata fields of a study.

    Parameters
    ----------
      species : bioturing_connector.typing.Species,
            Species of the study.\n
            Support:
              bioturing_connector.typing.Species.HUMAN.value\n
              bioturing_connector.typing.Species.MOUSE.value\n
              bioturing_connector.typing.Species.PRIMATE.value\n
              bioturing_connector.typing.Species.OTHERS.value\n
      study_id : str,
            uuidv4 of study
      group_id : str, optional. Default=None
            If you want to get metadata from a study in group "bioturing_public_studies",\n
            set group_id = 'bioturing_public_studies',\n
            otherwise, leave it as default.

    Returns
    ----------
      Metadata : pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
    }
    result = self.post_request(
      api_route='api/v1/study/get_metadata_fields',
      data=data
    )
    common.check_result_status(result)
    fields = result['data']
    return fields


  def get_metadata(
    self,
    species: str,
    study_id: str,
    group_id: str = None,
    fields: List[str] = []
  ):
    """
    Get full metadata of a study.

    Parameters
    ----------
      species : bioturing_connector.typing.Species,
            Species of the study.\n
            Support:
              bioturing_connector.typing.Species.HUMAN.value\n
              bioturing_connector.typing.Species.MOUSE.value\n
              bioturing_connector.typing.Species.PRIMATE.value\n
              bioturing_connector.typing.Species.OTHERS.value\n
      study_id : str,
            uuidv4 of study
      group_id : str, optional. Default=None
            If you want to get metadata from a study in group "bioturing_public_studies",\n
            set group_id = 'bioturing_public_studies',\n
            otherwise, leave it as default.
      fields : List[str], optional. Default=[]

    Returns
    ----------
      Metadata : pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'fields': fields,
    }
    result = self.post_request(
      api_route='api/v1/study/get_metadata',
      data=data
    )
    common.check_result_status(result)
    metadata_dict = result['data']
    metadata_df = pd.DataFrame(metadata_dict)
    return metadata_df


  def get_barcodes(
    self,
    species: str,
    study_id: str
  ):
    """
    Get barcodes of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,\n
          uuidv4 of study

    Returns
    ----------
    barcodes : List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_barcodes',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def get_features(
    self,
    species: str,
    study_id: str
  ):
    """
    Get features of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    Features : List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_features',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def list_all_custom_embeddings(
    self,
    species: str,
    study_id: str
  ):
    """
    List all custom embeddings of a study

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    List of embeddings' info : List[dict]
      In which:
        'embedding_id': the uuid used in further steps\n
        'embedding_name': displaying name on platform\n
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/list_all_custom_embeddings',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def retrieve_custom_embedding(
    self,
    species: str,
    study_id: str,
    embedding_id: str
  ):
    """
    Retrieve an embedding array of a study

    Parameters
    -------------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    embedding_id : str,
          Embedding id (uuid)

    Returns
    -------------
    embedding_arr : np.ndarray with shape (n_cells x n_dims)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'embedding_id': embedding_id
    }
    result = self.post_request(
      api_route='api/v1/retrieve_custom_embedding',
      data=data
    )
    common.check_result_status(result)
    coord_arr = result['data']['coord_arr']
    coord_shape = result['data']['coord_shape']
    return decode_base64_array(coord_arr, 'float32', coord_shape)


  def submit_metadata_from_dataframe(
    self,
    species: str,
    study_id: str,
    group_id: str,
    df: pd.DataFrame
  ):
    """
    Submit metadata dataframe directly to a study

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    df : pandas DataFrame,
          Barcodes must be in df.index!!!!

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    metadata_dct = common.dataframe2dictionary(df)
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'metadata_dct': metadata_dct
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_dataframe',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def submit_metadata_from_local(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str
  ):
    """
    Submit metadata to a study with local path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : local path leading to metadata file,
          Barcodes must be in the first column\n
          File suffix must be in .tsv/.csv

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    df = common.read_csv(file_path, index_col=0)
    return self.submit_metadata_from_dataframe(
      species,
      study_id,
      group_id,
      df
    )


  def submit_metadata_from_s3(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str,
    s3_id: str = None,
  ):
    """
    Submit metadata to a study with s3 path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : str,
          Path in s3 bucket leading to metadata file,\n
          Notes:
            Barcodes must be in the fist column\n
            File suffix must be in .tsv/.csv\n
            File_path DOES NOT contain s3_bucket path configured on the platform
              E.g:
                realpath: 's3://bucket/folder/metadata.tsv'\n
                inputpath: 'folder/metadata.tsv'
    s3_id : str, Optional
          ID of s3 bucket. Default: None\n
          If s3_id is not provided, we will use the first s3 bucket configured on the platform.

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'file_path': file_path,
      's3_id': s3_id,
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_s3',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def submit_metadata_from_shared_s3(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str,
    shared_s3_id: str = None,
  ):
    """
    Submit metadata to a study with s3 path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : str,
          Path in s3 bucket leading to metadata file,\n
          Notes:
            Barcodes must be in the fist column\n
            File suffix must be in .tsv/.csv\n
            File_path DOES NOT contain s3_bucket path configured on the platform
              E.g:
                realpath: 's3://bucket/prefix/metadata.tsv'\n
                inputpath: 'prefix/metadata.tsv'
    shared_s3_id : str
          ID of shared s3 bucket

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'file_path': file_path,
      'shared_s3_id': shared_s3_id,
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_from_shared_s3',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def get_ontologies_tree(
    self,
    species,
    group_id,
  ):
    """
    Get standardized ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value
    group_id : str
          ID of the group.

    Returns
    ----------
    Ontologies tree : Dict[Dict]
      In which:
        'name': name of the node, which will be used in further steps\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_ontologies',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def assign_standardized_meta(
    self,
    species,
    group_id,
    study_id,
    metadata_field,
    metadata_value,
    root_name,
    leaf_name,
  ):
    """
    Assign metadata value to a standardized term on ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id  : str
          ID of the group to submit the data to.
    study_id  : str
          ID of the study (uuid)
    metadata_field  : str
          ~ column name of meta dataframe in platform (eg: author's tissue)
    metadata_value  : str
          ~ metadata value within the metadata field (eg: normal lung)
    root_name : str
          name of root in btr ontologies tree (eg: tissue)
    leaf_name : str
          name of leaf in btr ontologies tree (eg: lung)

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    ontologies_tree = self.get_ontologies_tree(species, group_id)
    root_id, leaf_id = common.parse_root_leaf_name(
      ontologies_tree,
      root_name,
      leaf_name
    )
    data = {
      'species': species,
      'group_id': group_id,
      'study_id': study_id,
      'group': metadata_field,
      'name': metadata_value,
      'root_id': root_id,
      'leaf_id': leaf_id,
    }
    result = self.post_request(
      api_route='api/v1/study/assign_standardized_term',
      data=data
    )
    common.check_result_status(result)
    return 'Successul'

  def get_export_log(self, group_id: str, task_id: str):
    last_status = []
    while True:
      export_log = self.post_request(
        api_route='api/v1/get_submission_log',
        data={'task_id': task_id},
        check_error=False
      )
      message = self._get_error_message(export_log)
      if message:
        print(message)
        break

      current_status = export_log['data']['log'].split('\n')[:-1]
      new_status = current_status[len(last_status):]
      if len(new_status):
        print('\n'.join(new_status))

      last_status += new_status
      if export_log['data']['status'] != 'SUCCESS':
        time.sleep(5)
        continue
      else:
        res = self.post_request(
          api_route='api/v1/get_export_result',
          data={
            'group_id': group_id,
            'task_id': task_id
          },
          check_error=False
        )
        message = self._get_error_message(res)
        if message:
          print(message)
          break
        else:
          return {
            'status': True,
            'data': {
              'url': urljoin(self.__host, res['data']['file_path'].lstrip('/')),
              'file_name': res['data']['file_name']
            }
          }
    return False

  def get_download_study_url(
      self,
      group_id,
      study_id,
      study_type = StudyType.H5AD.value,
      species = Species.HUMAN.value,
    ):
    """
    Get the url of an exported study.

    Parameters
    ----------
    group_id : str
          ID of the group to which the study belongs.
    study_id : str
          The UUID of the study to be downloaded.
    study_type : str, optional
          Format of the study. Default: bioturing_connector.typing.StudyType.H5AD.value\n
          Support:
                bioturing_connector.typing.StudyType.H5AD.value\n
                bioturing_connector.typing.StudyType.RDS.value\n
    species : str, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    dest_path : str, optional
          The destination file path to save the downloaded study.
          If not provided, the default file name from the response will be used.

    Returns
    -------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'group_id': group_id,
      'study_id': study_id,
      'context': [],
      'study_type': study_type,
    }
    export_status = self.post_request(
      api_route='api/v1/export_study',
      data=data,
    )
    task_id = common.parse_submission_status(export_status)
    if task_id is None:
      return False

    res = self.get_export_log(
      group_id=group_id,
      task_id=task_id,
    )
    return res if res else False

  def download_study(
      self,
      group_id,
      study_id,
      study_type = StudyType.H5AD.value,
      species = Species.HUMAN.value,
      dest_path = None,
      chunk_size = ChunkSize.CHUNK_100_MB.value,
    ):
    """
    Download a private study.

    Parameters
    ----------
    group_id : str
          ID of the group to which the study belongs.
    study_id : str
          The UUID of the study to be downloaded.
    study_type : str, optional
          Format of the study. Default: bioturing_connector.typing.StudyType.H5AD.value\n
          Support:
                bioturing_connector.typing.StudyType.H5AD.value\n
                bioturing_connector.typing.StudyType.RDS.value\n
    species : str, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    dest_path : str, optional
          The destination file path to save the downloaded study.
          If not provided, the default file name from the response will be used.
    chunk_size : bioturing_connector.typing.ChunkSize, optional
          Size of each separated chunk for uploading. Default: 104857600\n
          Support:
                bioturing_connector.typing.ChunkSize.CHUNK_5_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_100_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_500_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_1_GB.value\n

    Returns
    -------
    Submission status : bool | str
      True or Error log
    """
    res = self.get_download_study_url(group_id, study_id, study_type, species)
    if not res:
      return res
    url = res['data']['url']
    dest_path = dest_path or res['data']['file_name']
    print('Downloading')
    response = requests.get(url, timeout=3600, stream=True)
    if response.status_code == 200:
      total_size = int(response.headers.get('content-length', 0))
      with open(dest_path, 'wb') as f, tqdm(
          desc=os.path.basename(dest_path),
          total=total_size,
          unit='iB',
          unit_scale=True,
          unit_divisor=1024,
        ) as progress:
        for chunk in response.iter_content(chunk_size=chunk_size):
          if not chunk:
            return False
          f.write(chunk)
          progress.update(len(chunk))
      print('DONE!')
      return True
    print('Failed to download', url)
    return False
