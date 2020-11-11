from IPC.Card import Card
from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Authorization(Base):
    """
* Process IPC method: IPCAuthorization.
* Collect, validate and send API params
    """
    __card: Card
    __currency = 'EUR'
    __amount: float
    __itemName: str
    __orderID: str
    __note: str


    def __init__(self, cnf: Config):
        """
    * Return purchase object
    *
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def setOrderID(self, orderID: str):
        """
    * Purchase identifier - must be unique
    *
    * @param string orderID
    *
    * @return Authorization
        """
        self.__orderID = orderID

        return self

    def setItemName(self, itemName: str):
        """
    * Item Name of the PreAuthorization
    *
    * @param mixed itemName
    *
    * @return Authorization
        """
        self.__itemName = itemName

        return self

    def setCurrency(self, currency: str):
        """
    * ISO-4217 Three letter __currency code
    *
    * @param string currency
    *
    * @return Authorization
        """
        self.__currency = currency

        return self

    def setAmount(self, amount: float):
        """
    * Total amount of the PreAuthorization
    *
    * @param mixed amount
    *
    * @return Authorization
        """
        self.__amount = amount

        return self

    def setCard(self, card: Card):
        """
    * Card object
    *
    * @param Card card
    *
    * @return Authorization
        """
        self.__card = card

        return self

    def setNote(self, note: str):
        """
    * Optional note to purchase
    *
    * @param string note
    *
    * @return Authorization
        """
        self.__note = note

        return self


    def process(self):
        """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCAuthorization')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())

        self._addPostParam('ItemName', self.getItemName())

        self._addPostParam('Amount', self.getAmount())
        self._addPostParam('Currency', self.getCurrency())

        self._addPostParam('CardToken', self.getCard().getCardToken())

        self._addPostParam('Note', self.getNote())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
        """
        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if not Helper.versionCheck(self._getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self._getCnf().getVersion() + ' does not support IPCAuthorization method. Please use 1.4 or above.')

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

    def getCurrency(self):
        """
    * ISO-4217 Three letter __currency code
    *
    * @return string
        """
        return self.__currency

    def getCard(self):
        """
    * Card object
    *
    * @return Card
        """
        return self.__card

    def getOrderID(self):
        """
    * Purchase identifier
    *
    * @return string
        """
        return self.__orderID

    def getItemName(self):
        """
    * Item Name for the PreAuthorization
    *
    * @return mixed
        """
        return self.__itemName

    def getAmount(self):
        """
    * Total amount of the PreAuthorization
    *
    * @return mixed
        """
        return self.__amount

    def getNote(self):
        """
    * Optional note to purchase
    *
    * @return string
        """
        return self.__note
