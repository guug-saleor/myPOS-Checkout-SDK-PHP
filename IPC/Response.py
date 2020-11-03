import base64
from typing import Dict
from IPC.Defines import Defines
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * IPC Response class. Parse and validate income __data
"""
class Response(object):
    """
    * @var Config
    """
    __cnf: Config
    __raw_data = None
    __format = None
    __data: Dict[str, str]
    __signature: str

    """
    *
    * @param cnf: Config
    * @param string|array raw_data
    * @param string format COMMUNICATION_FORMAT_JSON|COMMUNICATION_FORMAT_XML|COMMUNICATION_FORMAT_POST
    *
    * @raises IPC_Exception
    """
    def __init__(self, cnf: Config, raw_data, format):
        self.__cnf = cnf
        self.__setData(raw_data, format)

    """
    * @param raw_data
    * @param format
    *
    * @return self
    * @raises IPC_Exception
    """
    def __setData(self, raw_data, format):
        if not bool(raw_data):
            raise IPC_Exception('Invalid Response data')

        self.__format = format
        self.__raw_data = raw_data

        if format == Defines.COMMUNICATION_FORMAT_JSON:
            self.__data = Dict[str, str](json_decode(self.__raw_data, 1))
        elif format == Defines.COMMUNICATION_FORMAT_XML:
            self.__data = Dict[str, str](SimpleXMLElement(self.__raw_data))
            if self.__data['@attributes']):
                unset(self.__data['@attributes'])
        elif format == Defines.COMMUNICATION_FORMAT_POST:
            self.__data = self.__raw_data
        else:
            raise IPC_Exception('Invalid response format!')

        if not bool(self.__data):
            raise IPC_Exception('No IPC Response!')

        self.__extractSignature()

        if not bool(self.__signature) and array_key_exists('Status', self.__data) and self.__data['Status'] == Defines.STATUS_IPC_ERROR:
            raise IPC_Exception('IPC Response - General Error!')

        self.__verifySignature()

        return self

    def __extractSignature(self):
        # TODO: select one of (list, tuple)
        if bool(self.__data) and isinstance(self.__data, (list, tuple)):
            for k, v in self.__data :
                if strtolower(k) == '__signature':
                    self.__signature = v
                    unset(self.__data[k])

        return True

    """
    * @raises IPC_Exception
    """
    def __verifySignature(self):
        if not bool(self.__signature):
            raise IPC_Exception('Missing request __signature!')

        if not self.__cnf:
            raise IPC_Exception('Missing config object!')

        pubKeyId = openssl_get_publickey(self.__cnf.getAPIPublicKey())
        if (not openssl_verify(__getSignData(), base64.b64decode(self.__signature), pubKeyId, Defines.SIGNATURE_ALGO)):
            raise IPC_Exception('Signature check failed!')

    def __getSignData(self):
        return base64.b64encode(implode('-', Helper.getValuesFromMultiDimensionalArray(self.__data)))

    """
    * Static class to create Response object
    *
    * @param cnf: Config
    * @param string|array raw_data
    * @param string format
    *
    * @return Response
    * @raises IPC_Exception
    """
    @staticmethod
    def getInstance(cnf: Config, raw_data, format: str):
        return Response(cnf, raw_data, format)

    """
    * Validate Signature param from IPC response
    *
    * @return boolean
    """
    def isSignatureCorrect(self):
        try:
            self.__verifySignature()
        except Exception as ex:
            return False

        return True

    """
    * Request param: Signature
    *
    * @return string
    """
    def getSignature(self):
        return self.__signature

    #############################################

    """
    * Request param: Status
    *
    * @return int
    * @raises IPC_Exception
    """
    def getStatus(self):
        return Helper.getArrayVal(self.getData(str.lower), 'status')

    """
    * Return IPC Response in array
    *
    * @param function case str.lower|str.upper
    *
    * @return array
    * @raises IPC_Exception
    """
    def getData(self, case = None):
        if case != None:
            if (not case in [
                str.lower,
                str.upper,
            ]):
                raise IPC_Exception('Invalid Key Case!')

            return dict((case(k), v) for k, v in self.__data)
            # array_change_key_case(self.__data, case)

        return self.__data

    """
    * Request param: StatusMsg
    *
    * @return string
    * @raises IPC_Exception
    """
    def getStatusMsg(self):
        return Helper.getArrayVal(self.getData(str.lower), 'statusmsg')

    """
    * Return IPC Response in original format json/xml/array
    *
    * @return string|array
    """
    def getDataRaw(self):
        return self.__raw_data
