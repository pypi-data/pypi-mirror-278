from typing import Any
import json
import requests
from requests import Response
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def validate_type(variable: Any, expected_type: Any, variable_name: str) -> None:
    """
    Validates that the given variable is of the expected type or types.

    This function checks if the variable matches the expected type or any type in a tuple of expected types.
    It raises a TypeError if the variable does not match the expected type(s).

    Parameters:
        variable (Any): The variable to be checked.
        expected_type (Any): The expected type or a tuple of expected types.
        variable_name (str): The name of the variable, used in the error message to identify the variable.

    Raises:
        TypeError: If the variable is not of the expected type(s).

    Returns:
        None: This function does not return a value; it raises an exception if the type check fails.
    """

    if not isinstance(expected_type, tuple):
        expected_type = (expected_type,)

    expected_type_names = ', '.join(type_.__name__ for type_ in expected_type)

    if not any(isinstance(variable, type_) for type_ in expected_type):
        raise TypeError(
            f"{variable_name} must be of type '{expected_type_names}', but '{type(variable).__name__}' was provided")


def set_method_call(method):
    """
    Decorates a method to ensure it is properly registered and tracked within the builder's workflow.

    This decorator adds the method's name to a set that tracks method calls

    Parameters:
        method (function): The method to be decorated.

    Returns:
        function: The wrapped method with added functionality to register its call.

    Raises:
        None: This decorator does not raise exceptions by itself but ensures the method call is registered.
    """

    def wrapper(self, *args, **kwargs):
        self.method_calls.append(method.__name__)
        return method(self, *args, **kwargs)

    return wrapper


def parse_json(value):
    """
    Attempts to convert a string into a Python object by interpreting it as JSON.

    Args:
        value (str | Any): The value to attempt to convert. If the value is not a string,
                           it is returned directly without attempting conversion.

    Returns:
        Any: The Python object resulting from the JSON conversion if `value` is a valid JSON string.
             If the conversion fails due to a formatting error (ValueError), the original value is returned.
             If `value` is not a string, it is returned as is.
    """
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except ValueError:
        return value


def send_request(method: str, headers, url: str, payload: dict[str, Any] | str = None,
                 files: [str, [str, bytes, str]] = None) -> Response | str:
    """
    Helper function to make HTTP requests.

    This function simplifies making HTTP requests by handling different HTTP methods (POST, GET, PUT, DELETE) and managing common exceptions. It supports sending payloads and files as part of the request.

    Args:
        method (str): The HTTP method to use for the request ('post', 'get', 'put', 'delete').
        headers (dict): The headers to include in the request.
        url (str): The URL to which the request is sent.
        payload (dict[str, Any] | str, optional): The payload to include in the request body. Defaults to None.
        files ([str, [str, bytes, str]], optional): The files to include in the request. Defaults to None.

    Returns:
        Response | str: The response object from the request if successful, or an error message string if an exception occurs.

    Raises:
        ValueError: If an unsupported HTTP method is provided.
    """
    try:
        if method == 'post':
            response = requests.post(url, headers=headers, data=payload, files=files, verify=False,
                                     timeout=3000)
        elif method == 'get':
            response = requests.get(url, headers=headers, verify=False, timeout=3000)
        elif method == 'put':
            response = requests.put(url, headers=headers, data=payload, files=files, verify=False,
                                    timeout=3000)
        elif method == 'delete':
            response = requests.delete(url, headers=headers, verify=False, timeout=3000)
        else:
            raise ValueError(f'Unsupported HTTP method: {method}')

        return response
    except requests.exceptions.ConnectionError as conn_err:
        return f'Connection error: {str(conn_err)}'
    except requests.exceptions.Timeout as timeout_err:
        return f'Timeout error: {str(timeout_err)}'
    except requests.exceptions.RequestException as req_err:
        return f'Request exception: {str(req_err)}'
    except Exception as e:
        return f'Unexpected error: {str(e)}'


def handle_basic_response(response: requests.Response) -> dict[str, Any]:
    """
    Handle basic HTTP response.

    This function processes the HTTP response and returns a dictionary containing the status code. If the response indicates an error, it also includes the error message.

    Args:
        response (requests.Response): The response object to process.

    Returns:
        dict[str, Any]: A dictionary containing the status code and, if applicable, the error message.
    """
    if response.status_code in [200, 201]:
        return {'status_code': response.status_code}
    else:
        return {'status_code': response.status_code, 'error': response.text}
