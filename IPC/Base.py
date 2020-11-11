import abc
import socket
import ssl
from urllib.parse import urlencode
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64
from IPC.Config import Config
from IPC.Defines import Defines
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception
from IPC.Response import Response
from urllib.parse import urlparse, parse_qsl

class Base(metaclass=abc.ABCMeta):
    """
*  Base API Class. Contains basic API-connection methods.
    """
    """
    *  @var string Output format from API for some requests may be XML or JSON
    """
    _outputFormat = Defines.COMMUNICATION_FORMAT_JSON
    __cnf: Config
    """
    *  @var array Params for API Request
    """
    __params = {}

    @staticmethod
    def isValidSignature(data: str, signature: str, pubKey: str):
        """
    *  Verify signature of API Request __params against the API public key
    * 
    *  @param string data Signed data
    *  @param string signature Signature in base64 format
    *  @param string pubKey API public key
    * 
    *  @return boolean
        """
        pubKeyId = openssl_get_publickey(pubKey)
        res = openssl_verify(data, base64.b64decode(signature), pubKeyId, Defines.SIGNATURE_ALGO)
        openssl_free_key(pubKeyId)
        if res != 1:
            return False

        return True

    def getOutputFormat(self):
        """
    *  Return current set output format for API Requests
    * 
    *  @return string
        """
        return self._outputFormat

    def setOutputFormat(self, outputFormat: str):
        """
    *  Set current set output format for API Requests
    * 
    *  @param string outputFormat
        """
        self._outputFormat = outputFormat

    def _addPostParam(self, paramName: str, paramValue, encrypt = False):
        """
    *  Add API request param
    * 
    *  @param string paramName
    *  @param string paramValue
    *  @param bool encrypt
        """
        if not isinstance(paramValue, str):
            paramValue = str(paramValue)
        self.__params[paramName] = self.__encryptData(paramValue) if encrypt else Helper.escape(Helper.unescape(paramValue))

    def __encryptData(self, data: str):
        """
    *  Create signature of API Request __params against the SID private key
    * 
    *  @param string data
    * 
    *  @return string base64 encoded signature
        """
        openssl_public_encrypt(data, crypted, self._getCnf().getEncryptPublicKey(), Defines.ENCRYPT_PADDING)

        return base64.b64encode(crypted)

    def _getCnf(self):
        """
    *  Return IPC\Config object with current IPC configuration
    * 
    *  @return Config
        """
        return self.__cnf

    def _setCnf(self, cnf: Config):
        """
    *  Set Config object with current IPC configuration
    * 
    *  @param cnf: Config
        """
        self.__cnf = cnf

    def _processHtmlPost(self):
        """
    *  Generate HTML form with POST __params and auto-submit it
        """
        #Add request signature
        self.__params['Signature'] = self.__createSignature()

        c = '<body onload="document.ipcForm.submit()">'
        c += '<form id="ipcForm" name="ipcForm" action="' + self._getCnf().getIpcURL() + '" method="post">'
        for k, v in self.__params:
            c += "<input type=\"hidden\" name=\"" + k + "\" value=\"" + v + "\"  />\n"
        c += '</form></body>'
        print (c)
        exit

    def __createSignature(self):
        """
    *  Create signature of API Request __params against the SID private key
    * 
    *  @return string base64 encoded signature
        """
        __params = self.__params
        for k, v in __params:
            __params[k] = Helper.unescape(v)
        concData = base64.b64encode(implode('-', __params))
        privKey = openssl_get_privatekey(self._getCnf().getPrivateKey())
        openssl_sign(concData, signature, privKey, Defines.SIGNATURE_ALGO)

        return base64.b64encode(signature)

    def _processPost(self):
        """
    *  Send POST Request to API and returns Response object with validated response data
    * 
    *  @return Response
    *  @raises IPC_Exception
        """
        self.__params['Signature'] = self.__createSignature()
        url = urlparse(self._getCnf().getIpcURL())
        ssl = "" # JSON.parse({"url": ""})
        if not url.port:
            if url.scheme == 'https':
                url.port = 443
                ssl = "ssl://"
            else:
                url.port = 80
        postData = urlencode(self.__params)
        # TODO mayby add try catch construction
        # TODO: add ssl
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #tcp socket
        sock.connect((url.hostname, url.port))
        fp = sock.makefile()
        # fsockopen(f"{ssl}{url.hostname}", url.port, errno, errstr, 10)
        if not fp:
            raise IPC_Exception('Error connecting IPC URL')
        else:
            eol = "\r\n"
            path = url.path + ('' if (bool(url.query)) else ('?' + url.query))
            fp.write(f"POST {path} HTTP/1.1{eol}")
            fp.write(f"Host: {url.hostname}{eol}")
            fp.write(f"Content-type: application/x-www-form-urlencoded{eol}")
            fp.write(f"Content-length: {len(postData)}{eol}")
            fp.write(f"Connection: close{eol}{eol}")
            fp.write(f"{postData}{eol}{eol}")

            result = ''
            line = fp.readline(1024)
            while (line):
                result += line
                line = fp.readline(1024)
            fp.close()
            result = result.split("{eol}{eol}", 2)[:-2]
            header = result[0] if len(result) > 0 else ''
            cont = result[1] if len(result) > 1 else ''

            #Check Transfer-Encoding: chunked
            if bool(cont) and 'Transfer-Encoding: chunked' in header:
                check = self.__httpChunkedDecode(cont)
                if check:
                    cont = check
            if cont:
                cont = cont.strip()

            return Response.getInstance(self._getCnf(), cont, self._outputFormat)

    def __httpChunkedDecode(self, chunk: str):
        """
    *  Alternative of php http-chunked-decode function
    * 
    *  @param string chunk
    * 
    *  @return mixed
        """
        pos = 0
        len = len(chunk)
        dechunk = None
        newlineAt = chunk.find("\n", pos + 1)

        while pos < len and newlineAt:
            chunkLenHex = chunk[pos:pos + newlineAt - pos]
            if self.__is_hex(chunkLenHex):
                return False

            pos = newlineAt + 1
            chunkLen = int(chunkLenHex.rstrip("\r\n"), 16)
            dechunk += chunk[pos:pos + chunkLen]
            pos = chunk.find("\n", pos + chunkLen) + 1
            newlineAt = chunk.find("\n", pos + 1)


        return dechunk

    def __is_hex(_self, hex: str):
        """
    *  determine if a string can represent a number in hexadecimal
    * 
    *  @param string hex
    * 
    *  @return boolean True if the string is a hex, otherwise False
        """
        # regex is for weenies
        hex = hex.lstrip("0").strip().lower()
        if not bool(hex):
            hex = "0"
        dec = int(hex, 16)

        return hex == "%x" % dec
