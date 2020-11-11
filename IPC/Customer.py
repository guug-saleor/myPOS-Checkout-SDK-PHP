from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception
from IPC.Purchase import Purchase


class Customer(object):
    """
 * Customer details class.
 * Collect and validate client details
    """
    __email: str
    __phone: str
    __firstName: str
    __lastName: str
    __country: str
    __city: str
    __zip: str
    __address: str

    def getPhone(self):
        """
    * Customer Phone number
    *
    * @return string
        """
        return self.__phone

    def setPhone(self, phone: str):
        """
    * Customer Phone number
    *
    * @param string phone
    *
    * @return Customer
        """
        self.__phone = phone

        return self

    def getCountry(self):
        """
    * Customer country code ISO 3166-1
    *
    * @return string
        """
        return self.__country

    def setCountry(self, country: str):
        """
    * Customer country code ISO 3166-1
    *
    * @param string country
    *
    * @return Customer
        """
        self.__country = country

        return self

    def getCity(self):
        """
    * Customer city
    *
    * @return string
        """
        return self.__city

    def setCity(self, city: str):
        """
    * Customer city
    *
    * @param string city
    *
    * @return Customer
        """
        self.__city = city

        return self

    def getZip(self):
        """
    * Customer ZIP code
    *
    * @return string
        """
        return self.__zip

    def setZip(self, zip: str):
        """
    * Customer ZIP code
    *
    * @param string zip
    *
    * @return Customer
        """
        self.__zip = zip

        return self

    def getAddress(self):
        """
    * Customer address
    *
    * @return string
        """
        return self.__address

    def setAddress(self, address: str):
        """
    * Customer address
    *
    * @param string address
    *
    * @return Customer
        """
        self.__address = address

        return self

    def validate(self, paymentParametersRequired):
        """
    * Validate all set customer details
    *
    * @param string paymentParametersRequired
    *
    * @return bool
    * @raises IPC_Exception
        """
        if paymentParametersRequired == Purchase.PURCHASE_TYPE_FULL:

            if self.getFirstName() == None:
                raise IPC_Exception('Invalid First name')

            if self.getLastName() == None:
                raise IPC_Exception('Invalid Last name')

            if self.getEmail() == None or not Helper.isValidEmail(self.getEmail()):
                raise IPC_Exception('Invalid Email')

        return True

    def getFirstName(self):
        """
    * Customer first name
    *
    * @return string
        """
        return self.__firstName

    def setFirstName(self, firstName: str):
        """
    * Customer first name
    *
    * @param string firstName
    *
    * @return Customer
        """
        self.__firstName = firstName

        return self

    def getLastName(self):
        """
    * Customer last name
    *
    * @return string
        """
        return self.__lastName

    def setLastName(self, lastName: str):
        """
    * Customer last name
    *
    * @param string lastName
    *
    * @return Customer
        """
        self.__lastName = lastName

        return self

    def getEmail(self):
        """
    * Customer Email address
    *
    * @return string
        """
        return self.__email

    def setEmail(self, email: str):
        """
    * Customer Email address
    *
    * @param string email
    *
    * @return Customer
        """
        self.__email = email

        return self
