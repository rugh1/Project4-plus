"""
Author: Rugh1
Date: 25.01.2024
Description: web server for project 4
"""
import re
import socket
import rughhttp
import logging
import server_functions
from comm import *
# Configure logging
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_URL = '/'
QUEUE_SIZE = 10
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 2
WEBROOT = 'webroot'

PATH_FUNCTIONS = {
    '/moved': 'moved',
    '/error': 'error',
    '/forbidden': 'forbidden',
    '/calculate-next':'calculate_next',
    '/calculate-area' : 'calculate_area',
    '/upload':'post_file',
    '/image': 'get_file'
    # Add more paths and functions as needed
}

def handle_client(client_socket):
    """
    Handle a connection from a client.

    :param client_socket: The socket connected to the client.
    :type client_socket: socket.socket

    :return: None    :rtype:
    """
    logging.info("New client connection")
    try:
        req = recv(client_socket)
        logging.debug("Received request: %s", req)
        if len(req) > 0:
            if valid_get(req):
                req = parse_http_request(req)
                if req.method == 'POST':
                    req.body = recv_body(client_socket, int(req.header['Content-Length']))
                create_response = getattr(server_functions, PATH_FUNCTIONS.get(req.path, 'others'))
                res = create_response(req)
            else:
                res = rughhttp.HttpRespond(400, {}).to_binary()
            logging.info("Sending response: %s", res)
            client_socket.send(res)
    except Exception as e:
        logging.error("Error handling request: %s",  str(e))
        print(str(e))
    finally:
        client_socket.close()
        logging.info("Client connection closed")


def valid_get(request_string):
    """
    Check if a GET or POST request is valid.

    :param request_string: The GET request string.
    :type request_string: str

    :return: True if the GET request is valid, False otherwise.
    :rtype: bool
    """
    pattern1 = r"^GET (.*) HTTP/1.1"
    pattern2 = r"^POST (.*) HTTP/1.1"
    match = re.match(pattern1, request_string)
    if match is None:
         match = re.match(pattern2, request_string)
    return match is not None


def parse_http_request(request):
    if request.startswith('GET'):
        return rughhttp.HttpGet(request)
    return rughhttp.HttpPost(request)

def main():
    """
    Main function to run the server.

    :return: None    :rtype:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        logging.info("Listening for connections on port %d", PORT)
        print("Listening for connections on port %d" % PORT)
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print("New connection received from %s" % str(client_address))
                client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                logging.error("Received socket exception: %s", err)
            except Exception as err:
                logging.error("Error handling connection: %s", err)
            finally:
                client_socket.close()
    except socket.error as err:
        logging.error("Received socket exception: %s", err)
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
    #print(rugh_http.HttpGet.get_parm_from_url('GET /calculate-next?num=101 HTTP/1.1'))