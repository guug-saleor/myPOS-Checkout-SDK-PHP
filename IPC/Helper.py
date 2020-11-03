from IPC.Defines import Defines
import re


"""
*  IPC Library helper functions
"""
class Helper(object):
    def __init__(_self):
        pass

    """
    *  Validate email address
    * 
    *  @param string email
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidEmail(email):
        return filter_var(email, FILTER_VALIDATE_EMAIL)

    """
    *  Validate URL address
    * 
    *  @param string url
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidURL(url):
        return filter_var(url, FILTER_VALIDATE_URL)

    """
    *  Validate IP address
    * 
    *  @param string ip
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidIP(ip):
        return filter_var(ip, FILTER_VALIDATE_IP)

    """
    *  Validate customer names
    * 
    *  @param string name
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidName(name):
        return re.search("/^[a-zA-Z ]*/", name)

    """
    *  Validate amount.
    * 
    *  @param float amt
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidAmount(amt):
        return re.search('/^(-)?[0-9]+(?:\.[0-9]{0,2})?/', amt)

    """
    *  Validate quantity
    * 
    *  @param int quantity
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidCartQuantity(quantity):
        return isinstance(quantity, int) and quantity > 0

    """
    *  Validate transaction reference
    * 
    *  @param string trnref
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidTrnRef(trnref):
        #TODO
        return True

    """
    *  Validate Order ID
    * 
    *  @param string trnref
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidOrderId(trnref):
        #TODO
        return True

    """
    *  Validate output format
    * 
    *  @param string outputFormat
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidOutputFormat(outputFormat):
        return (outputFormat in [
            Defines.COMMUNICATION_FORMAT_XML,
            Defines.COMMUNICATION_FORMAT_JSON,
        ])

    """
    *  Validate card number
    * 
    *  @param cardNo
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidCardNumber(cardNo):
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

    """
    *  Validate card CVC
    * 
    *  @param cvc
    * 
    *  @return boolean
    """
    @staticmethod
    def isValidCVC(cvc):
        return (cvc.isnumeric() and len(cvc) == 3)

    @staticmethod
    def versionCheck(current, required):
        return (int)str_replace('.', '', current) >= (int)str_replace('.', '', required)

    """
    *  Escape HTML special chars
    * 
    *  @param string text
    * 
    *  @return string type
    """
    @staticmethod
    def escape(text):
        text = htmlspecialchars_decode(text, ENT_QUOTES)

        return htmlspecialchars(text, ENT_QUOTES)

    """
    *  Unescape HTML special chars
    * 
    *  @param string text
    * 
    *  @return string
    """
    @staticmethod
    def unescape(text):
        return htmlspecialchars_decode(text, ENT_QUOTES)

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
    @staticmethod
    def getArrayVal(array, key, default = '', notEmpty = False):
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

    """
    *  Returns one-dimensional array with all values from multi-dimensional array
    *  Useful when create request signature where only array values matter
    * 
    *  @param array array
    *  @param array values
    * 
    *  @return array
    """
    @staticmethod
    def getValuesFromMultiDimensionalArray(array, values = []):
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
