from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCPreAuthorizationStatus.
 * Collect, validate and send API params
"""
class PreAuthorizationStatus(Base):
    __orderID: str

    """
    * Return purchase object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Purchase identifier - must be unique
    *
    * @param string orderID
    *
    * @return PreAuthorizationStatus
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPreAuthStatus')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())

        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if not Helper.versionCheck(self.getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self.getCnf().getVersion() + ' does not support IPCPreAuthorizationStatus method. Please use 1.4 or above.')

        return True

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID
