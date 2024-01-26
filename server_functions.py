"""
Author: Rugh1
Date: 26.01.2024
Description: web server for project 4
"""
from rugh_http import *
def moved(get_request):
    return HttpRespond(302, {'Location': '/'}).to_binary()


def error(get_request):
    return HttpRespond(500, {}).to_binary()


def forbidden(get_request):
    return HttpRespond(403, {}).to_binary()


def others(get_request):
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
     if get_request.parm.get('num', None) != None and get_request.parm['num'].isdigit():
        return HttpRespond(200, {}, (str(int(get_request.parm['num'])+1)).encode(), Rugh_http.content_types['txt']).to_binary()
     return HttpRespond(400, {}).to_binary()


def calculate_area(get_request):
    print(get_request.parm)
    if get_request.parm.get('height', None) != None and get_request.parm.get('width', None) != None:
        if get_request.parm['height'].isdigit() and get_request.parm['width'].isdigit():
            return HttpRespond(200, {}, (str((int(get_request.parm['width']) * int(get_request.parm['height']))/2)).encode(), Rugh_http.content_types['txt']).to_binary()
    return HttpRespond(400, {}).to_binary()


def post_file(get_request):
    try:
        f = open(f'webroot/upload/{get_request.parm["file-name"]}', 'wb')
        f.write(get_request.body)
        return HttpRespond(200, {}).to_binary()
    except Exception as err:
        print(err)
        return HttpRespond(400, {}).to_binary()

def get_file(get_request):
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
    data = b''
    with open(file_path, "rb") as f:
                data = f.read()
    return data


    # def create_response(self):
    #     """
    #         Creates an HTTP response for the GET request.

    #         :return: The HTTP response.
    #         :rtype: HttpRespond
    #     """
    #     if self.path == '/':
    #         self.path = '/index.html'
    #     file_path = self.WEB_ROOT + self.path
    #     print(file_path)
    #     logging.info("Creating response for path: %s", self.path)
    #     if self.path == '/moved':
    #         print('moving')
    #         return HttpRespond(302, {'Location': '/'})
    #     if self.path == '/error':
    #         return HttpRespond(500, {})
    #     if self.path == '/forbidden':
    #         return HttpRespond(403, {})
    #     if os.path.isfile(file_path):
    #         print("found")
    #         with open(file_path, "rb") as f:
    #             file = f.read()
    #             print(len(file))
    #             content_type = self.content_types[file_path.split('.')[-1]]
    #         return HttpRespond(200, {}, file, content_type)
    #     else:
    #         print("notfound")
    #         file_path = 'webroot/404.html'
    #         with open(file_path, "rb") as f:
    #             file = f.read()
    #             print(len(file))
    #             content_type = self.content_types[file_path.split('.')[-1]]
    #         return HttpRespond(404, {}, file, content_type)