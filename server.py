import re
import socket
import rugh_http
import logging

# Configure logging
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_URL = '/'
QUEUE_SIZE = 10
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 2
WEBROOT = 'webroot'


def handle_client(client_socket):
    """
    Handle a connection from a client.

    :param client_socket: The socket connected to the client.
    :type client_socket: socket.socket

    :return: None    :rtype:
    """
    logging.info("New client connection")
    try:
        req = client_socket.recv(1024).decode()
        logging.debug("Received request: %s", req)
        if len(req) > 0:
            if valid_get(req):
                req = rugh_http.HttpGet(req)
                res = req.create_response()
            else:
                res = rugh_http.HttpRespond(400, {})
                print(res.to_binary().decode())
            logging.info("Sending response: %s %s", res.line, res.header)
            client_socket.send(res.to_binary())
    except Exception as e:
        logging.error("Error handling request: %s", e)
    finally:
        client_socket.close()
        logging.info("Client connection closed")


def valid_get(request_string):
    """
    Check if a GET request is valid.

    :param request_string: The GET request string.
    :type request_string: str

    :return: True if the GET request is valid, False otherwise.
    :rtype: bool
    """
    pattern = r"^GET (.*) HTTP/1.1"
    match = re.match(pattern, request_string)
    print(request_string)
    return match is not None


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