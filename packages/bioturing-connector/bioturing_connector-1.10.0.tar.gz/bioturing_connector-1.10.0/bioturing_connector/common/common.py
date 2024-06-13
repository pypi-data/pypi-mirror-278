import pandas as pd
from scipy import sparse

from . import decode_base64_array


def check_result_status(result):
  if not result:
    raise ConnectionError('Connection failed')

  if 'status' not in result:
    raise ValueError(result['detail'])

  if result['status'] != 200:
    if 'message' in result:
      raise Exception(f"Something went wrong: {result['message']}")
    else:
      raise Exception('Something went wrong')


def parse_submission_status(submission_status):
  """
    Parse submission status response
  """
  if not submission_status:
    print('Connection failed')
    return None

  if 'status' not in submission_status:
    if 'detail' in submission_status:
      print (submission_status['detail'])
    else:
      print('Internal server error. Please check server log.')
    return None

  if submission_status['status'] != 200:
    if 'message' in submission_status:
      print(f"Submission failed. {submission_status['message']}")
      return None
    else:
      print('Submission failed.')
      return None

  return submission_status['data']['id']


def parse_query_genes_result(query_genes_result):
  """Parse query genes result
  """
  check_result_status(query_genes_result)

  indptr = decode_base64_array(query_genes_result['data']['indptr'], 'uint64')
  indices = decode_base64_array(query_genes_result['data']['indices'], 'uint32')
  data = decode_base64_array(query_genes_result['data']['data'], 'float32')
  shape = query_genes_result['data']['shape']
  csc_mtx = sparse.csc_matrix((data, indices, indptr), shape=shape)
  return csc_mtx


def dataframe2dictionary(df):
  res = dict()
  res['barcodes'] = df.index.values.tolist()
  for column in df.columns:
    tmp_data = df.loc[:, column].values
    try:
      data = [int(x) for x in tmp_data]
    except:
      data = [str(x) for x in tmp_data]
    res[column] = data
  return res


def read_csv(path, **kwargs):
  df = pd.read_csv(filepath_or_buffer = path, sep='\t', **kwargs)

  if 'index_col' in kwargs:
    if len(df.columns) == 0:
      return pd.read_csv(filepath_or_buffer = path, sep=',', **kwargs)
  else:
    if len(df.columns) < 2:
      return pd.read_csv(filepath_or_buffer = path, sep=',', **kwargs)

  return df


def parse_root_leaf_name(
    ontologies_tree,
    root_name,
    leaf_name,
  ):
  root_ids = []
  for id in ontologies_tree['tree']:
    if ontologies_tree['tree'][id]['name'] == root_name:
      root_ids.append(id)
  for root_id in root_ids:

    children = ontologies_tree['tree'][root_id]['children']
    for child in children:
      if child['name'] == leaf_name:
        leaf_id = child['id']
        return root_id, leaf_id

      grand_children = child['children']
      for grand_child in grand_children:
        if grand_child['name'] == leaf_name:
          leaf_id = grand_child['id']
          return root_id, leaf_id

  raise Exception('Cannot find "{}" - "{}"'.format(root_name, leaf_name))
