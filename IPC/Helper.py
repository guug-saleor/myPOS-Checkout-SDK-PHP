from IPC.Defines import Defines
import re


class Helper(object):
    """
*  IPC Library helper functions
    """
    def __init__(_self):
        pass

    @staticmethod
    def isValidEmail(email):
        """
    *  Validate email address
    * 
    *  @param string email
    * 
    *  @return boolean
        """
        return filter_var(email, FILTER_VALIDATE_EMAIL)


    @staticmethod
    def isValidURL(url):
        """
    *  Validate URL address
    * 
    *  @param string url
    * 
    *  @return boolean
        """
        return filter_var(url, FILTER_VALIDATE_URL)


    @staticmethod
    def isValidIP(ip):
        """
    *  Validate IP address
    * 
    *  @param string ip
    * 
    *  @return boolean
        """
        return filter_var(ip, FILTER_VALIDATE_IP)


    @staticmethod
    def isValidName(name):
        """
    *  Validate customer names
    * 
    *  @param string name
    * 
    *  @return boolean
        """
        return re.search("/^[a-zA-Z ]*/", name)


    @staticmethod
    def isValidAmount(amt):
        """
    *  Validate amount.
    * 
    *  @param float amt
    * 
    *  @return boolean
        """
        return re.search('/^(-)?[0-9]+(?:\.[0-9]{0,2})?/', amt)


    @staticmethod
    def isValidCartQuantity(quantity):
        """
    *  Validate quantity
    * 
    *  @param int quantity
    * 
    *  @return boolean
        """
        return isinstance(quantity, int) and quantity > 0


    @staticmethod
    def isValidTrnRef(trnref):
        """
    *  Validate transaction reference
    * 
    *  @param string trnref
    * 
    *  @return boolean
        """
        #TODO
        return True


    @staticmethod
    def isValidOrderId(trnref):
        """
    *  Validate Order ID
    * 
    *  @param string trnref
    * 
    *  @return boolean
        """
        #TODO
        return True


    @staticmethod
    def isValidOutputFormat(outputFormat):
        """
    *  Validate output format
    * 
    *  @param string outputFormat
    * 
    *  @return boolean
        """
        return (outputFormat in [
            Defines.COMMUNICATION_FORMAT_XML,
            Defines.COMMUNICATION_FORMAT_JSON,
        ])


    @staticmethod
    def isValidCardNumber(cardNo):
        """
    *  Validate card number
    * 
    *  @param cardNo
    * 
    *  @return boolean
        """
        cardNo = cardNo.strip().replace(" ", "")
        if (not cardNo.isnumeric()) or (len(cardNo) > 19) or (len(cardNo) < 13):
            return False
        sum = dub = add = chk = 0
        even = 0
        for i in range(len(cardNo) - 1, -1, -1):
            if even == 1:
                dub = 2 * cardNo[i]
                if dub > 9:
                    add = dub - 9
                else:
                    add = dub
                even = 0
            else:
                add = cardNo[i]
                even = 1
            sum += add

        return ((sum % 10) == 0)


    @staticmethod
    def isValidCVC(cvc):
        """
    *  Validate card CVC
    * 
    *  @param cvc
    * 
    *  @return boolean
        """
        return (cvc.isnumeric() and len(cvc) == 3)

    @staticmethod
    def versionCheck(current, required):
        return (int)str_replace('.', '', current) >= (int)str_replace('.', '', required)


    @staticmethod
    def escape(text):
        """
    *  Escape HTML special chars
    * 
    *  @param string text
    * 
    *  @return string type
        """
        text = htmlspecialchars_decode(text, ENT_QUOTES)

        return htmlspecialchars(text, ENT_QUOTES)


    @staticmethod
    def unescape(text):
        """
    *  Unescape HTML special chars
    * 
    *  @param string text
    * 
    *  @return string
        """
        return htmlspecialchars_decode(text, ENT_QUOTES)


    @staticmethod
    def getArrayVal(array, key, default = '', notEmpty = False):
        """
    *  Return associative array element by key.
    *  If key not found in array returns default
    *  If notEmpty argument is TRUE returns default even if key is found in array but the element has empty value(0, None, '')
    * 
    *  @param array array
    *  @param mixed key
    *  @param string default
    *  @param bool notEmpty
    * 
    *  @return mixed
        """
        # TODO: select one of (list, tuple)
        if not isinstance(array, (list, tuple)):
            return default
        if notEmpty:
            if array_key_exists(key, array):
                val = trim(array[key])
                if bool(val):
                    return val

            return default
        else:
            return array[key] if array_key_exists(key, array) else default


    @staticmethod
    def getValuesFromMultiDimensionalArray(array, values = []):
        """
    *  Returns one-dimensional array with all values from multi-dimensional array
    *  Useful when create request signature where only array values matter
    * 
    *  @param array array
    *  @param array values
    * 
    *  @return array
        """
        # TODO: select one of (list, tuple)
        if not isinstance(array, (list, tuple)):
            return values
        for k, v in array:
            # TODO: select one of (list, tuple)
            if isinstance(v, (list, tuple)):
                values = Helper.getValuesFromMultiDimensionalArray(v, values)
            else:
                values += v

        return values
