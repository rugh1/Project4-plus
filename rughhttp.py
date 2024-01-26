"""
Author: Rugh1
Date: 25.01.2024
Description: classes for http GET and POST request and respond and general 
"""
import os
import logging

# Configure logging
logging.basicConfig(filename='http_server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RughHttp:
    WEB_ROOT = 'webroot'
    STATUS_CODES = {
        100: 'Continue',
        101: 'Switching Protocols',
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        206: 'Partial Content',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Moved Temporarily',
        304: 'Not Modified',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Conflict',
        429: 'Too Many Requests',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout'
    }
    content_types = {
        'html': 'text/html',  # HTML
        'jpg': 'image/jpeg',  # JPEG
        'css': 'text/css',  # CSS
        'js': 'application/javascript',  # JavaScript
        'txt': 'text/plain',  # Text
        'ico': 'image/x-icon',  # ICO
        'gif': 'image/jpeg',  # GIF
        'png': 'image/png',  # PNG
        'mp3': 'audio/mpeg'  # MP3
    }

    def __init__(self, http_text=None, line=None, header=None, body=None):
        """
        Initializes an instance of the Http class.

        :return: None        :rtype:
        """
        if http_text is not None:
            self.line, self.header, self.body = self.parse_http_request(http_text)
            self.header = self.convert_header_to_dict(self.header)
        else:
            self.line = line
            self.header = header
            self.body = body

    def to_binary(self):
        """
        Converts the HTTP instance to binary format.

        :return: The binary representation of the HTTP instance.
        :rtype: bytes
        """
        if self.body is None:
            return f"{self.line}\r\n{self.convert_header_to_string(self.header)}\r\n".encode()
        return f"{self.line}\r\n{self.convert_header_to_string(self.header)}\r\n".encode() + self.body

    @staticmethod
    def parse_http_request(request):
        """
        Parses an HTTP request.

        :param request: The raw HTTP request.
        :type request: str

        :return: The HTTP request line, headers, and body.
        :rtype: tuple
        """
        logging.debug("Parsing HTTP request: %s", request)
        line, header, body = '', '', ''
        if request.find('\r\n') == -1:
            line = request
        elif request.find('\r\n\r\n') == -1:
            header = request[request.find('\r\n') + 4:]
        else:
            line = request[0:request.find('\r\n')]
            header = request[request.find('\r\n') + 4:request.find('\r\n\r\n')]
            body = request[request.find('\r\n\r\n') + 8:]
        logging.debug("Parsing HTTP request: %s, %s, %s", line, header, body)
        return line, header, body

    @staticmethod
    def convert_header_to_string(header):
        """
        Converts HTTP headers to a string.

        :param header: The HTTP headers.
        :type header: dict

        :return: The string representation of HTTP headers.
        :rtype: str
        """
        logging.debug("Converting header to string: %s", header)
        headers = ""
        for key, value in header.items():
            headers += f"{key}: {value}\r\n"
            logging.debug("Converted header to string: %s", headers)
        return headers


    @staticmethod
    def convert_header_to_dict(header):
        """
        Converts HTTP headers from string to dict.

        :param header: The HTTP headers as string.
        :type header: str

        :return: The dict representation of HTTP headers.
        :rtype: dict
        """
        header = header.split("\r\n")
        headers = {p.split(':')[0] : p.split(':')[1] for p in header}
        return headers



class HttpRespond(RughHttp):
    def __init__(self, code, header, body=None, content_type=None):
        """
        Initializes an instance of the HttpRespond class.

        :return: None        :rtype:
        """
        self.line = f"HTTP/1.1 {code} {self.STATUS_CODES[code]}"
        self.header = header
        self.body = body
        if body is None:
            return
        self.handle_data(content_type)

    def handle_data(self, content_type):
        """
            Handles data in the response.

            :return: None            :rtype:
        """
        self.header.update({'Content-Type': content_type})
        self.header.update({'Content-Length': str(len(self.body))})
        return


class HttpGet(RughHttp):
    method = 'GET'
    REDIRECTION_DICTIONARY = {
        '/moved': '/index.html'
    }

    def __init__(self, http_text):
        """
            Initializes an instance of the HttpGet class.

            :return: None            :rtype:
        """
        super().__init__(http_text=http_text)
        self.parm = self.get_parm_from_url(self.line) 
        self.path = self.get_path_from_url(self.line)
        print(self.path)

    @staticmethod
    def get_path_from_url(url):
        """
            Extracts the path from the URL.

            :param url: The URL.
            :type url: str

            :return: The path from the URL.
            :rtype: str
        """
        logging.debug("Extracting path from URL: %s", url)
        url = url.split(" ")[1].split('?')[0]
        return url
    
    @staticmethod
    def get_parm_from_url(url):
        """
            Extracts the paramters from the URL.

            :param url: The URL.
            :type url: str

            :return: The paramters of the url.
            :rtype: dictionry of parmaters in string format
        """
        parm_str = url.split('?')
        if len(parm_str) > 1:
            parm_str = parm_str[1]
            print(parm_str)
            parm_str = parm_str.split(" ")
            parm_str.pop()
            parm_str = ' '.join(parm_str)
            print(parm_str)
            parm = {p.split('=')[0] : p.split('=')[1] for p in parm_str.split('&')}
            return parm

class HttpPost(RughHttp):
    method = 'POST'
    def __init__(self, http_text):
        """
            Initializes an instance of the HttpGet class.

            :return: None            :rtype:
        """
        super().__init__(http_text=http_text)
        self.parm = self.get_parm_from_url(self.line) 
        self.path = self.get_path_from_url(self.line)

    @staticmethod
    def get_path_from_url(url):
        """
            Extracts the path from the URL.

            :param url: The URL.
            :type url: str

            :return: The path from the URL.
            :rtype: str
        """
        logging.debug("Extracting path from URL: %s", url)
        url = url.split(" ")[1].split('?')[0]
        return url
    
    @staticmethod
    def get_parm_from_url(url):
        """
            Extracts the paramters from the URL.

            :param url: The URL.
            :type url: str

            :return: The paramters of the url.
            :rtype: dictionry of parmaters in string format
        """
        parm_str = url.split('?')
        if len(parm_str) > 1:
            parm_str = parm_str[1]
            print(parm_str)
            parm_str = parm_str.split(" ")
            parm_str.pop()
            parm_str = ' '.join(parm_str)
            print(parm_str)
            parm = {p.split('=')[0] : p.split('=')[1] for p in parm_str.split('&')}
            return parm