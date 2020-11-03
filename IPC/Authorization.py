from IPC.Card import Card
from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
* Process IPC method: IPCAuthorization.
* Collect, validate and send API params
"""


class Authorization(Base):
    """
    * @var Card
    """
    __card: Card
    __currency = 'EUR'
    __amount: float
    __itemName: str
    __orderID: str
    __note: str


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
    * @return Authorization
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Item Name of the PreAuthorization
    *
    * @param mixed itemName
    *
    * @return Authorization
    """
    def setItemName(self, itemName: str):
        self.__itemName = itemName

        return self

    """
    * ISO-4217 Three letter __currency code
    *
    * @param string currency
    *
    * @return Authorization
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    * Total amount of the PreAuthorization
    *
    * @param mixed amount
    *
    * @return Authorization
    """
    def setAmount(self, amount: float):
        self.__amount = amount

        return self

    """
    * Card object
    *
    * @param Card card
    *
    * @return Authorization
    """
    def setCard(self, card: Card):
        self.__card = card

        return self

    """
    * Optional note to purchase
    *
    * @param string note
    *
    * @return Authorization
    """
    def setNote(self, note: str):
        self.__note = note

        return self


    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCAuthorization')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())

        self._addPostParam('ItemName', self.getItemName())

        self._addPostParam('Amount', self.getAmount())
        self._addPostParam('Currency', self.getCurrency())

        self._addPostParam('CardToken', self.getCard().getCardToken())

        self._addPostParam('Note', self.getNote())
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
            raise IPC_Exception('IPCVersion ' + self.getCnf().getVersion() + ' does not support IPCAuthorization method. Please use 1.4 or above.')

        if self.getItemName() == None or not isinstance(self.getItemName(), str):
            raise IPC_Exception('Empty or invalid item name.')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid __currency')

        if self.getAmount() == None or not Helper.isValidAmount(self.getAmount()):
            raise IPC_Exception('Empty or invalid amount')

        if self.getCard() == None:
            raise IPC_Exception('Missing card details')

        if self.getCard().getCardNumber() != None:
            raise IPC_Exception('IPCAuthorization supports only card token.')

        try:
            self.getCard().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Card details: {ex}')

        return True

    """
    * ISO-4217 Three letter __currency code
    *
    * @return string
    """
    def getCurrency(self):
        return self.__currency

    """
    * Card object
    *
    * @return Card
    """
    def getCard(self):
        return self.__card

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * Item Name for the PreAuthorization
    *
    * @return mixed
    """
    def getItemName(self):
        return self.__itemName

    """
    * Total amount of the PreAuthorization
    *
    * @return mixed
    """
    def getAmount(self):
        return self.__amount

    """
    * Optional note to purchase
    *
    * @return string
    """
    def getNote(self):
        return self.__note
