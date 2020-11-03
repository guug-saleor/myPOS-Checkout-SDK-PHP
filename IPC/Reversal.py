from IPC.Config import Config
from IPC.Base import Base
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCReversal.
 * Collect, validate and send API params
"""
class Reversal(Base):
    __trnref: str

    """
     * Return Refund object
     *
     * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
     * Initiate API request
     *
     * @return Response
     * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCReversal')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())
        self._addPostParam('IPC_Trnref', self.getTrnref())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    """
     * Validate all set refund details
     *
     * @return boolean
     * @raises IPC_Exception
    """
    def validate(self):
        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getTrnref() == None or not Helper.isValidTrnRef(self.getTrnref()):
            raise IPC_Exception('Invalid TrnRef')

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    """
     * Transaction reference - transaction unique identifier
     *
     * @return string
    """
    def getTrnref(self):
        return self.__trnref

    """
     * Transaction reference - transaction unique identifier
     *
     * @param string trnref
     *
     * @return Reversal
    """
    def setTrnref(self, trnref: str):
        self.__trnref = trnref

        return self
