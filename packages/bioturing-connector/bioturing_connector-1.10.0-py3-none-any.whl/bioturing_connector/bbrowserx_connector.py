"""Python package for submitting/getting data from BBrowserX"""

from pathlib import Path

from typing import List
from typing import Union

from .common import common
from .common import get_uuid
from .common.constants import UNKNOWN

from .typing import Species
from .typing import StudyType
from .typing import ChunkSize
from .typing import InputMatrixType

from .connector import Connector


class BBrowserXConnector(Connector):
  """
  Create a connector object to submit/get data from BBrowserX

  Parameters
  ----------
  host : `str`
    The URL of the BBrowserX server, only support HTTPS connection\n
    Example:
      https://talk2data.bioturing.com/t2d_index_tool/
  token : `str`
    The API token to verify authority. Generated in-app.
  """


  def _check_study_type(self, study_type):
    if study_type not in [
      StudyType.BBROWSER.value,
      StudyType.H5_10X.value,
      StudyType.H5AD.value,
      StudyType.MTX_10X.value,
      StudyType.BCS.value,
      StudyType.RDS.value,
      StudyType.TSV.value,
      StudyType.TILE_DB.value,
    ]:
      raise Exception('Unsupported study_type, please recheck the imported connector \n(should be BBrowserXConnector for this study_type)')


  def _submit_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    input_matrix_type: str = InputMatrixType.NORMALIZED.value,
    study_type: int = StudyType.H5AD.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    mt_percentage: Union[int, float] = None,
    skip_dimred: bool = False,
  ):
    if study_id is None:
      study_id = get_uuid()

    if min_counts is None:
      min_counts = 0

    if min_genes is None:
      min_genes = 0

    if max_counts is None:
      max_counts = 1e9

    if max_genes is None:
      max_genes = 1e9

    if mt_percentage is None:
      mt_percentage = 100

    study_info = {
      'study_hash_id': study_id,
      'name': name,
      'authors': authors if authors else [],
      'abstract': abstract
    }

    return {
      'species': species,
      'group_id': group_id,
      'filter_params': {
        'min_counts': min_counts,
        'min_genes': min_genes,
        'max_counts': max_counts,
        'max_genes': max_genes,
        'mt_percentage': mt_percentage / 100
      },
      'study_type': study_type,
      'normalize': input_matrix_type == InputMatrixType.RAW.value,
      'subsample': -1,
      'skip_dimred': skip_dimred,
      'study_info': study_info,
    }


  def _submit_processed_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
  ):
    if study_id is None:
      study_id = get_uuid()

    study_info = {
      'study_hash_id': study_id,
      'name': name,
      'authors': authors if authors else [],
      'abstract': abstract
    }

    return {
      'species': species,
      'group_id': group_id,
      'filter_params': {
        'min_counts': UNKNOWN,
        'min_genes': UNKNOWN,
        'max_counts': UNKNOWN,
        'max_genes': UNKNOWN,
        'mt_percentage': UNKNOWN,
      },
      'study_type': StudyType.PROCESSED_FOLDER.value,
      'study_info': study_info,
    }


  def submit_study_from_s3(
      self,
      group_id: str,
      s3_id: str = None,
      batch_info: List[dict] = [],
      study_id: str = None,
      name: str = 'TBD',
      authors: List[str] = [],
      abstract: str = '',
      species: str = Species.HUMAN.value,
      input_matrix_type: str = InputMatrixType.NORMALIZED.value,
      study_type: int = StudyType.H5AD.value,
      min_counts: int = None,
      min_genes: int = None,
      max_counts: int = None,
      max_genes: int = None,
      mt_percentage: Union[int, float] = None,
      skip_dimred: bool = False
    ):
    """
    Submit one or multiple datasets from s3 bucket to BBrowserX.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    s3_id : str, Optional
          ID of s3 bucket. Default: None\n
          If s3_id is not provided, we will use the first s3 bucket configured on the platform.
    batch_info : List[dict]
          File path and batch name information, the path DOES NOT included the bucket path!\n
          Example:
            For h5ad format:
              [{
                'matrix': 's3_path/GSE128223_1.h5ad'
              }, {...}]
            For mtx format:
              [{
                'matrix': 's3_path/data_1/matrix.mtx',\n
                'features': 's3_path/data_1/features.tsv',\n
                'barcodes': 's3_path/data_1/barcodes.tsv',
              }, {...}]
            For tiledb format:
              [{
                'folder': 's3_path/GSE128223_1'
              }, {...}]
    study_id : str, optional
          Will be the displaying name of study (eg: PBMC_3K). Default: uuidv4
    name : str, optional
          Name of the study. Default: 'TBD'
    authors : List[str], optional
          Authors of the study. Default: []
    abstract : str, optional
          Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    skip_dimred : Bool, optional
          Skip BioTuring pipeline if set to True. Default: False\n
          (only applicable when input is a scanpy/seurat object).
    input_matrix_type : bioturing_connector.typing.InputMatrixType, optional
          Is the input matrix already normalized or not?. Default: 'normalized'\n
          Support:
                bioturing_connector.typing.InputMatrixType.NORMALIZED.value
                  (will skip BioTuring normalization, h5ad: use adata.X)
                bioturing_connector.typing.InputMatrixType.RAW.value
                  (apply BioTuring normalization, h5ad: use adata.raw.X)
    study_type : bioturing_connector.typing.StudyType, opitonal
          Format of the study. Default: bioturing_connector.typing.StudyType.H5AD.value\n
          Support:
                bioturing_connector.typing.StudyType.BBROWSER.value\n
                bioturing_connector.typing.StudyType.H5_10X.value\n
                bioturing_connector.typing.StudyType.H5AD.value\n
                bioturing_connector.typing.StudyType.MTX_10X.value\n
                bioturing_connector.typing.StudyType.BCS.value\n
                bioturing_connector.typing.StudyType.RDS.value\n
                bioturing_connector.typing.StudyType.TSV.value\n
                bioturing_connector.typing.StudyType.TILE_DB.value\n
    min_counts : int, optional
          Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
          Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
          Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
          Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    mt_percentage : int, optional
          Maximum number of mitochondria genes percentage required for a cell to pass filtering. Default: 100\n
          Ranging from 0 to 100\n

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    self._check_study_type(study_type)
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      input_matrix_type,
      study_type,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      mt_percentage,
      skip_dimred,
    )

    if study_type == StudyType.MTX_10X.value:
      for i, o in enumerate(batch_info):
        name = o['matrix'].split('/')
        if len(name) == 1:
          o['name'] = f'Batch {i + 1}'
        else:
          o['name'] = name[-2]
    elif study_type == StudyType.TILE_DB.value:
      for i, o in enumerate(batch_info):
        o['name'] = o['folder'].split('/')[-1]
    else:
      for i, o in enumerate(batch_info):
        o['name'] = o['matrix'].split('/')[-1]

    data['batch_info'] = {f'Batch_{i}': o for i, o in enumerate(batch_info)}
    data['s3_id'] = s3_id

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_s3',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id,
    )


  def submit_study_from_shared_s3(
      self,
      group_id: str,
      shared_s3_id: str,
      batch_info: List[dict] = [],
      study_id: str = None,
      name: str = 'TBD',
      authors: List[str] = [],
      abstract: str = '',
      species: str = Species.HUMAN.value,
      input_matrix_type: str = InputMatrixType.NORMALIZED.value,
      study_type: int = StudyType.H5AD.value,
      min_counts: int = None,
      min_genes: int = None,
      max_counts: int = None,
      max_genes: int = None,
      mt_percentage: Union[int, float] = None,
      skip_dimred: bool = False
    ):
    """
    Submit one or multiple datasets from s3 bucket to BBrowserX.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    shared_s3_id : str
          ID of s3 bucket.
    batch_info : List[dict]
          File path and batch name information, the path DOES NOT included the bucket path!\n
          Example:
            For h5ad format:
              [{
                'matrix': 's3_path/GSE128223_1.h5ad'
              }, {...}]
            For mtx format:
              [{
                'matrix': 's3_path/data_1/matrix.mtx',\n
                'features': 's3_path/data_1/features.tsv',\n
                'barcodes': 's3_path/data_1/barcodes.tsv',
              }, {...}]
            For tiledb format:
              [{
                'folder': 's3_path/GSE128223_1'
              }, {...}]
    study_id : str, optional
          Will be the displaying name of study (eg: PBMC_3K). Default: uuidv4
    name : str, optional
          Name of the study. Default: 'TBD'
    authors : List[str], optional
          Authors of the study. Default: []
    abstract : str, optional
          Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    skip_dimred : Bool, optional
          Skip BioTuring pipeline if set to True. Default: False\n
          (only applicable when input is a scanpy/seurat object).
    input_matrix_type : bioturing_connector.typing.InputMatrixType, optional
          Is the input matrix already normalized or not?. Default: 'normalized'\n
          Support:
                bioturing_connector.typing.InputMatrixType.NORMALIZED.value
                  (will skip BioTuring normalization, h5ad: use adata.X)
                bioturing_connector.typing.InputMatrixType.RAW.value
                  (apply BioTuring normalization, h5ad: use adata.raw.X)
    study_type : bioturing_connector.typing.StudyType, opitonal
          Format of the study. Default: bioturing_connector.typing.StudyType.H5AD.value\n
          Support:
                bioturing_connector.typing.StudyType.BBROWSER.value\n
                bioturing_connector.typing.StudyType.H5_10X.value\n
                bioturing_connector.typing.StudyType.H5AD.value\n
                bioturing_connector.typing.StudyType.MTX_10X.value\n
                bioturing_connector.typing.StudyType.BCS.value\n
                bioturing_connector.typing.StudyType.RDS.value\n
                bioturing_connector.typing.StudyType.TSV.value\n
                bioturing_connector.typing.StudyType.TILE_DB.value\n
    min_counts : int, optional
          Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
          Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
          Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
          Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    mt_percentage : int, optional
          Maximum number of mitochondria genes percentage required for a cell to pass filtering. Default: 100\n
          Ranging from 0 to 100\n

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    self._check_study_type(study_type)
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      input_matrix_type,
      study_type,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      mt_percentage,
      skip_dimred,
    )

    if study_type == StudyType.MTX_10X.value:
      for i, o in enumerate(batch_info):
        name = o['matrix'].split('/')
        if len(name) == 1:
          o['name'] = f'Batch {i + 1}'
        else:
          o['name'] = name[-2]
    elif study_type == StudyType.TILE_DB.value:
      for i, o in enumerate(batch_info):
        o['name'] = o['folder'].split('/')[-1]
    else:
      for i, o in enumerate(batch_info):
        o['name'] = o['matrix'].split('/')[-1]

    data['batch_info'] = {f'Batch_{i}': o for i, o in enumerate(batch_info)}
    data['shared_s3_id'] = shared_s3_id

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_shared_s3',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id,
    )


  def submit_study_from_local(
    self,
    group_id: str,
    batch_info: object,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    input_matrix_type: str = InputMatrixType.NORMALIZED.value,
    study_type: int = StudyType.H5AD.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    mt_percentage: Union[int, float] = None,
    skip_dimred: bool = False,
    chunk_size: int = ChunkSize.CHUNK_100_MB.value
  ):
    """
    Submit one or multiple datasets from local / server.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    batch_info : List[dict]
          File path and batch name information.\n
          Example:
            For h5ad format:
              [{
                'matrix': 'local_path/GSE128223_1.h5ad'
              }, {...}]
            For mtx format:
              [{
                'name': 'data_1',\n
                'matrix': 'local_path/data_1/matrix.mtx',\n
                'features': 'local_path/data_1/features.tsv',\n
                'barcodes': 'local_path/data_1/barcodes.tsv',
              }, {...}]
    study_id : str, optional
          Will be the displaying name of study (eg: PBMC_3K). Default: uuidv4
    name : str, optional
          Name of the study. Default: 'TBD'
    authors : List[str], optional
          Authors of the study. Default: []
    abstract : str, optional
          Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    input_matrix_type : bioturing_connector.typing.InputMatrixType, optional
          Is the input matrix already normalized or not?. Default: 'normalized'\n
          Support:
              bioturing_connector.typing.InputMatrixType.NORMALIZED.value
                (will skip BioTuring normalization, h5ad: use adata.X)
              bioturing_connector.typing.InputMatrixType.RAW.value
                (apply BioTuring normalization, h5ad: use adata.raw.X)
    study_type : bioturing_connector.typing.StudyType, optional
          Format of the study. Default: bioturing_connector.typing.StudyType.H5AD.value\n
          Support:
                bioturing_connector.typing.StudyType.BBROWSER.value\n
                bioturing_connector.typing.StudyType.H5_10X.value\n
                bioturing_connector.typing.StudyType.H5AD.value\n
                bioturing_connector.typing.StudyType.MTX_10X.value\n
                bioturing_connector.typing.StudyType.BCS.value\n
                bioturing_connector.typing.StudyType.RDS.value\n
                bioturing_connector.typing.StudyType.TSV.value\n
    min_counts : int, optional
          Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
          Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
          Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
          Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    mt_percentage : int, optional
          Maximum number of mitochondria genes percentage required for a cell to pass filtering. Default: 100.\n
          Ranging from 0 to 100
    skip_dimred : bool, optional
          Skip BioTuring pipeline if set to True (only appliable when input is a scanpy/seurat object). Default: False
    chunk_size : bioturing_connector.typing.ChunkSize, optional
          Size of each separated chunk for uploading. Default: 104857600\n
          Support:
                bioturing_connector.typing.ChunkSize.CHUNK_5_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_100_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_500_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_1_GB.value\n

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    if study_type == StudyType.TILE_DB.value:
      return 'Tile_db submission is only supported through s3 or shared s3'

    self._check_study_type(study_type)

    if chunk_size not in [e.value for e in ChunkSize]:
      return 'only support:\n{},\n{},\n{},\n{}'.format(
        'ChunkSize.CHUNK_5_MB.value',
        'ChunkSize.CHUNK_100_MB.value',
        'ChunkSize.CHUNK_500_MB.value',
        'ChunkSize.CHUNK_1_GB.value',
      )

    file_names = []
    files = []
    if study_type == StudyType.MTX_10X.value:
      for o in batch_info:
        file_names.extend([
          f'{o["name"]}matrix.mtx{".gz" if ".gz" in o["matrix"] else ""}',
          f'{o["name"]}features.tsv{".gz" if ".gz" in o["features"] else ""}',
          f'{o["name"]}barcodes.csv{".gz" if ".gz" in o["barcodes"] else ""}'
        ])
        files.extend([
          Path(o['matrix']),
          Path(o['features']),
          Path(o['barcodes'])
        ])
    else:
      for o in batch_info:
        p = Path(o['matrix'])
        o['name'] = p.name
        file_names.append(p.name)
        files.append(p)


    output_dir = self.upload_chunk(
      file_names,
      files,
      chunk_size
    )
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      input_matrix_type,
      study_type,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      mt_percentage,
      skip_dimred,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [o['name'] for o in batch_info]

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_local',
      data=data,
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id,
    )


  def submit_processed_study_from_local(
    self,
    group_id: str,
    folder_path: str,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    chunk_size: int = ChunkSize.CHUNK_100_MB.value
  ):
    """
    Submit one or multiple datasets from local / server.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    folder_path : str
          Path to processed folder.
    study_id : str, optional
          Will be the displaying name of study (eg: PBMC_3K). Default: uuidv4
    name : str, optional
          Name of the study. Default: 'TBD'
    authors : List[str], optional
          Authors of the study. Default: []
    abstract : str, optional
          Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
          Species of the study. Default: 'human'\n
          Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    chunk_size : bioturing_connector.typing.ChunkSize, optional
          Size of each separated chunk for uploading. Default: 104857600\n
          Support:
                bioturing_connector.typing.ChunkSize.CHUNK_5_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_100_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_500_MB.value\n
                bioturing_connector.typing.ChunkSize.CHUNK_1_GB.value\n

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    if chunk_size not in [e.value for e in ChunkSize]:
      return 'only support:\n{},\n{},\n{},\n{}'.format(
        'ChunkSize.CHUNK_5_MB.value',
        'ChunkSize.CHUNK_100_MB.value',
        'ChunkSize.CHUNK_500_MB.value',
        'ChunkSize.CHUNK_1_GB.value',
      )

    output_dir = self.upload_folder(folder_path, chunk_size)

    data = self._submit_processed_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
    )
    data['study_path'] = output_dir

    submission_status = self.post_request(
      api_route='api/v1/submit_processed_study_from_local',
      data=data,
    )
    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id,
    )