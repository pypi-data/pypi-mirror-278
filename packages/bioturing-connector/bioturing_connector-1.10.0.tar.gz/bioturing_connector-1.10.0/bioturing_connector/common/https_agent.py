"""A python class for performing HTTPS requests (GET, POST)"""

import http
import requests
import base64

class RequestError(Exception):
  """Exception for request error"""
  pass


class HttpsAgent:
  """Wrapper class of requests"""
  def __init__(self, token: str, ssl: bool):
    self.__token = token
    self.__ssl = ssl


  def get(self, url: str, params: dict = None):
    """Perform GET request

      Args:
        url:
          An API endpoint
          Example: https://bioturing.com/api
        params:
          Params of the GET requests, will be encoded to URL's query string
          Example: {"param1": 0, "param2": true}
    """
    if params is None:
      params = {}

    try:
      res = requests.get(
        url=url,
        params=params,
        headers={'bioturing-api-token': self.__token},
        verify=self.__ssl
      )
      return res.json()
    except requests.exceptions.RequestException as e:
      print('Request fail with error: ', e)
      return None


  def post(self, url: str, body: dict = None, check_error: bool = True):
    """
    Perform POST request

    Args:
      url:
        An API endpoint
        Example: https://bioturing.com/api

      body:
        Body of the request
        Example: {"param1": 0, "param2": true}
    """
    body = body if body is not None else {}

    res = requests.post(
      url=url,
      json=body,
      headers={'bioturing-api-token': self.__token},
      verify=self.__ssl,
      timeout=120,
    )

    try:
      res.raise_for_status()
      return res.json()
    except requests.exceptions.HTTPError:
      status = res.status_code
      try:
        error_detail = res.json()
      except requests.JSONDecodeError:
        error_detail = {}

      detail = error_detail.get('detail', http.client.responses[status])
      traceback = error_detail.get('traceback', 'None')
      message = f"Request failed with status {status}, {detail}\ntraceback: {traceback}"
      if check_error:
        raise RequestError(message)
