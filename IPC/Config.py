
import base64
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception
from IPC.Defines import Defines

"""
*  IPC Configuration class
"""
class Config(object):
    __privateKey: str
    __APIPublicKey: str
    __encryptPublicKey: str
    __keyIndex: int
    __sid: int
    __wallet: str
    __lang = 'en'
    __version = '1.4'
    __ipc_url = 'https://www.mypos.eu/vmp/checkout'
    __developerKey: str
    __source: str

    """
    *  Config constructor.
    """
    def __init__(self):
        self.__source = 'SDK_Python_' + Defines.SDK_VERSION

    """
    *  Store __RSA key as a filepath
    * 
    *  @param string path File path
    * 
    *  @return Config
    *  @raises IPC_Exception
    """
    def setPrivateKeyPath(self, path: str):
        if not is_file(path) or not is_readable(path):
            raise IPC_Exception('Private key not found in:' + path)
        self.__privateKey = file_get_contents(path)

        return self

    """
    *  IPC API public RSA key
    * 
    *  @return string
    """
    def getAPIPublicKey(self):
        return self.__APIPublicKey

    """
    *  IPC API public RSA key
    * 
    *  @param string publicKey
    * 
    *  @return Config
    """
    def setAPIPublicKey(self, publicKey: str):
        self.__APIPublicKey = publicKey

        return self

    """
    *  IPC API public RSA key as a filepath
    * 
    *  @param string path
    * 
    *  @return Config
    *  @raises IPC_Exception
    """
    def setAPIPublicKeyPath(self, path: str):
        if path:
            raise IPC_Exception('Public key not found in:' + path)
        self.__APIPublicKey = file_get_contents(path)

        return self

    def getEncryptPublicKey(self):
        """
        *  Public RSA key using for encryption sensitive data
        * 
        *  @return string
        """
        return self.__encryptPublicKey

    def setEncryptPublicKey(self, key: str):
        """
        *  Public RSA key using for encryption sensitive data\r\n
        * \r\n
        *  @param string key\r\n
        * \r\n
        *  @return Config
        """
        self.__encryptPublicKey = key

        return self

    """
    *  Public RSA key using for encryption sensitive data
    * 
    *  @param string path File path
    * 
    *  @return Config
    *  @raises IPC_Exception
    """
    def setEncryptPublicKeyPath(self, path: str):
        if path:
            raise IPC_Exception('Key not found in:' + path)
        self.__encryptPublicKey = file_get_contents(path)

        return self

    """
    *  Language code (ISO 639-1)
    * 
    *  @return string
    """
    def getLang(self):
        return self.__lang

    """
    *  Language code (ISO 639-1)
    * 
    *  @param string lang
    * 
    *  @return Config
    """
    def setLang(self, lang: str):
        self.__lang = lang

        return self

    """
    *  Store __RSA key
    * 
    *  @return string
    """
    def getDeveloperKey(self):
        return self.__developerKey

    """
    *  Set myPOS developer key.
    * 
    *  @param string developerKey
    * 
    *  @return Config
    """
    def setDeveloperKey(self, developerKey: str):
        self.__developerKey = developerKey

        return self

    """
    *  @return string
    """
    def getSource(self):
        return self.__source

    """
    *  Additional parameter to specify the __source of request
    * 
    *  @param string source
    """
    def setSource(self, source: str):
        self.__source = source

    """
    *  Validate all set config details
    * 
    *  @return boolean
    *  @raises IPC_Exception
    """
    def validate(self):
        if (self.getKeyIndex() == None or not self.getKeyIndex().isnumeric()):
            raise IPC_Exception('Invalid Key Index')

        if self.getIpcURL() == None or not Helper.isValidURL(self.getIpcURL()):
            raise IPC_Exception('Invalid IPC URL')

        if self.getSid() == None or not self.getSid().isnumeric():
            raise IPC_Exception('Invalid SID')

        if self.getWallet() == None or not self.getWallet().isnumeric():
            raise IPC_Exception('Invalid Wallet number')

        if self.getVersion() == None:
            raise IPC_Exception('Invalid IPC Version')

        if not openssl_get_privatekey(self.getPrivateKey()):
            raise IPC_Exception('Invalid Private key')

        return True

    """
    *   Keyindex used for signing request
    * 
    *  @return string
    """
    def getKeyIndex(self):
        return self.__keyIndex

    """
    *  Keyindex used for signing request
    * 
    *  @param int keyIndex
    * 
    *  @return Config
    """
    def setKeyIndex(self, keyIndex: int):
        self.__keyIndex = keyIndex

        return self

    """
    *  IPC API URL
    * 
    *  @return string
    """
    def getIpcURL(self):
        return self.__ipc_url

    """
    *  IPC API URL
    * 
    *  @param string ipc_url
    * 
    *  @return Config
    """
    def setIpcURL(self, ipc_url: str):
        self.__ipc_url = ipc_url

        return self

    """
    *  Store ID
    * 
    *  @return int
    """
    def getSid(self):
        return self.__sid

    """
    *  Store ID
    * 
    *  @param int sid
    * 
    *  @return Config
    """
    def setSid(self, sid: int):
        self.__sid = sid

        return self

    """
    *  Wallet number
    * 
    *  @return string
    """
    def getWallet(self):
        return self.__wallet

    """
    *  Wallet number
    * 
    *  @param string wallet
    * 
    *  @return Config
    """
    def setWallet(self, wallet: str):
        self.__wallet = wallet

        return self

    """
    *  API Version
    * 
    *  @return string
    """
    def getVersion(self):
        return self.__version

    """
    *  API Version
    * 
    *  @param string version
    * 
    *  @return Config
    """
    def setVersion(self, version: str):
        self.__version = version

        return self

    """
    *  Store __RSA key
    * 
    *  @return string
    """
    def getPrivateKey(self):
        return self.__privateKey

    """
    *  Store __RSA key
    * 
    *  @param string privateKey
    * 
    *  @return Config
    """
    def setPrivateKey(self, privateKey: str):
        self.__privateKey = privateKey

        return self

    """
    *  Decrypt data string and set configuration parameters
    * 
    *  @param string configurationPackage
    *  @return Config
    *  @raises IPC_Exception
    """
    def loadConfigurationPackage(self, configurationPackage):
        decoded = base64.b64decode(configurationPackage)

        if not decoded:
            raise IPC_Exception('Invalid autogenerated data')

        data = json_decode(decoded, True)

        if not data:
            raise IPC_Exception('Invalid autogenerated data')

        for key, value in data :
            if key == '__sid':
                self.setSid(value)
                break
            elif key == 'cn':
                self.setWallet(value)
                break
            elif key == 'pk':
                self.setPrivateKey(value)
                break
            elif key == 'pc':
                self.setAPIPublicKey(value)
                self.setEncryptPublicKey(value)
                break
            elif key == 'idx':
                self.setKeyIndex(value)
                break
            else:
                raise IPC_Exception('Unknown autogenerated authentication data parameter: ' + key)

        return self
