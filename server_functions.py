"""
Author: Rugh1
Date: 26.01.2024
Description: web server for project 4
"""
from rughhttp import *
def moved(get_request):
    """
    Generates a 302 Moved response.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    return HttpRespond(302, {'Location': '/'}).to_binary()


def error(get_request):
    """
    Generates a 500 Internal Server Error response.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    return HttpRespond(500, {}).to_binary()


def forbidden(get_request):
    """
    Generates a 403 Forbidden response.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    return HttpRespond(403, {}).to_binary()


def others(get_request):
    """
    Handles various HTTP requests for existing resources or returns a 404 response for non-existing resources.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    file_path = get_request.WEB_ROOT + get_request.path
    if get_request.path == '/':
         file_path = get_request.WEB_ROOT + '/index.html'
    if os.path.isfile(file_path):
        content_type = get_request.content_types[file_path.split('.')[-1]]
        data = get_data_from_file(file_path)
        return HttpRespond(200, {}, data, content_type).to_binary()
    file_path = 'webroot/404.html'
    content_type = get_request.content_types[file_path.split('.')[-1]]
    data = get_data_from_file(file_path)
    return HttpRespond(404 , {}, data, content_type).to_binary()


def calculate_next(get_request):
    """
    Calculates the next number based on the 'num' parameter in the GET request.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    if get_request.parm.get('num', None) is not None and get_request.parm['num'].isdigit():
        return HttpRespond(200, {}, (str(int(get_request.parm['num'])+1)).encode(),
                           RughHttp.content_types['txt']).to_binary()
    return HttpRespond(400, {}).to_binary()


def calculate_area(get_request):
    """
    Calculates the area based on the 'height' and 'width' parameters in the GET request.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    print(get_request.parm)
    if get_request.parm.get('height', None) is not None and get_request.parm.get('width', None) is not None:
        if get_request.parm['height'].isdigit() and get_request.parm['width'].isdigit():
            return HttpRespond(200, {}, (str((int(get_request.parm['width']) * int(get_request.parm['height']))/2)).encode(), RughHttp.content_types['txt']).to_binary()
    return HttpRespond(400, {}).to_binary()


def post_file(get_request):
    """
    Handles a POST request to upload a file.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    try:
        f = open(f'webroot/upload/{get_request.parm["file-name"]}', 'wb')
        f.write(get_request.body)
        return HttpRespond(200, {}).to_binary()
    except Exception as err:
        print(err)
        return HttpRespond(400, {}).to_binary()

def get_file(get_request):
    """
    Handles a GET request to retrieve a file.

    :param get_request: The HTTP GET request.
    :type get_request: HttpGet

    :return: The binary representation of the HTTP response.
    :rtype: bytes
    """
    try:
        print('aaaa')
        f = open(f'webroot/upload/{get_request.parm["image-name"]}', 'rb')
        data = f.read()
        print('aaaa1')
        return HttpRespond(200, {}, data, get_request.parm["image-name"].split('.')[-1]).to_binary()
    except FileNotFoundError:
        file_path = 'webroot/404.html'
        content_type = get_request.content_types[file_path.split('.')[-1]]
        data = get_data_from_file(file_path)
        return HttpRespond(404 , {}, data, content_type).to_binary()
    except Exception as err:
        print(err)
        return HttpRespond(400, {}).to_binary()
    

def get_data_from_file(file_path):
    """
    Reads and retrieves data from a file.

    :param file_path: The path of the file.
    :type file_path: str

    :return: The binary data read from the file.
    :rtype: bytes
    """
    data = b''
    with open(file_path, "rb") as f:
                data = f.read()
    return data