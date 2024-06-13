import os

import requests
from requests import Response


def write_to_file(
    file_path: str,
    content,
    encoding: str = 'utf-8'
) -> None:
    """
    Write some contents to a specific file.
    :param encoding:
    :param file_path:
    :param content:
    :return:
    """
    dir_path = os.path.dirname(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(file_path, 'w', encoding=encoding) as file:
        file.write(content)


def read_from_file(
    file_path: str,
    encoding: str = 'utf-8'
) -> any:
    """
    Read from a file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The file at path "{file_path}" was not found.')

    if not os.path.isfile(file_path):
        raise ValueError(f'The file at path "{file_path}" is not actually a fail.')

    with open(file_path, encoding=encoding, errors=None) as f:
        return f.read()


def read_from_url(
    url: str,
    bearer_token: str = None
) -> Response:
    """
    Read from url.
    """
    headers = {}

    if bearer_token:
        headers['Authorization'] = f'Bearer {bearer_token}'

    return requests.get(url, headers=headers)
