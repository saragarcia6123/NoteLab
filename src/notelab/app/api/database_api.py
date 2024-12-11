"""
This class is responsible for formulating and making requests to the server.
It is used for internal API requests
"""

import requests
from utils.app_config import Config

config = Config()

server_url = config.server_url
endpoints = config.database_endpoints
root = endpoints.root

method_to_request_function_map = {
    'get': requests.get,
    'post': requests.post,
    'delete': requests.delete,
    'put': requests.put,
}

"""Replaces parameter placeholders with the corresponding values"""
def format_endpoint_template(endpoint_template: str, **params) -> str:
    for key, value in params.items():
        placeholder = f"<string:{key}>"
        endpoint_template = endpoint_template.replace(placeholder, value)
    return endpoint_template

"""Makes the request to the server"""
def _make_request(endpoint, method, params=None) -> tuple[dict, int]:
    try:
        request_url = f"{server_url}{endpoint}"
        request_func = method_to_request_function_map.get(method.lower())
        if not request_func:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response = request_func(url=request_url, json=params)
        response.raise_for_status()
        return response.json(), response.status_code

    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")
        return {"error": str(req_err)}, 500

    except Exception as e:
        print('Error occurred:', e)
        return {"error": str(e)}, 500

"""Requests a list of tables from the Database"""
def get_tables():
    endpoint = root + endpoints['database']['tables']
    method = 'GET'
    return _make_request(endpoint, method)

"""Creates a table's column definitions in the Database"""
def create_table(table_name, columns):
    endpoint_template = root + endpoints['database']['table']
    endpoint = format_endpoint_template(endpoint_template, table_name=table_name)
    method = 'POST'
    params = {'columns': columns}
    return _make_request(endpoint, method, params)

"""Erases a table from the Database"""
def drop_table(table_name):
    endpoint_template = root + endpoints['database']['table']
    endpoint = format_endpoint_template(endpoint_template, table_name=table_name)
    method = 'DELETE'
    return _make_request(endpoint, method)

"""Inserts new rows into an existing table in the Database"""
def insert_rows(table_name, rows):
    endpoint_template = root + endpoints['database']['rows']
    endpoint = format_endpoint_template(endpoint_template, table_name=table_name)
    method = 'POST'
    params = {'rows': rows}
    return _make_request(endpoint, method, params)

"""Updates existing rows in an existing table in the Database"""
def update_rows(table_name, rows):
    endpoint_template = root + endpoints['database']['rows']
    endpoint = format_endpoint_template(endpoint_template, table_name=table_name)
    method = 'PUT'
    params = {'rows': rows}
    return _make_request(endpoint, method, params)