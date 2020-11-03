


"""
*  Container for SDK constants
"""
class Defines(object):
    COMMUNICATION_FORMAT_XML = 'xml'
    COMMUNICATION_FORMAT_JSON = 'json'
    COMMUNICATION_FORMAT_POST = 'post'
    SIGNATURE_ALGO = "sha256" # OPENSSL_ALGO_SHA256
    STATUS_SUCCESS = 0
    STATUS_MISSING_REQ_PARAMS = 1
    STATUS_SIGNATURE_FAILED = 2
    STATUS_IPC_ERROR = 3
    STATUS_INVALID_SID = 4
    STATUS_INVALID_PARAMS = 5
    STATUS_INVALID_REFERER = 6
    STATUS_PAYMENT_TRIES = 7
    STATUS_TRANSACTION_AUTH_FAIL = 8
    STATUS_WRONG_AMOUNT = 9
    STATUS_UNSUPPORTED_CALL = 10
    STATUS_INACTIVE_MANDATE_REFERENCE = 11
    STATUS_INVALID_MANDATE_REFERENCE = 12
    STATUS_NOT_SUFFICIENT_FUNDS = 13
    STATUS_TRANSACTION_NOT_PERMITTED = 14
    STATUS_EXCEEDED_LIMIT = 15
    STATUS_MANDATE_ALREADY_REGISTERED = 16
    STATUS_INACTIVE_ACOUNTIDENTIFIER = 17
    STATUS_INVALID_ACOUNTIDENTIFIER = 18
    STATUS_EXCEEDED_ACCOUNT_LIMITS = 19
    STATUS_DUPLICATE_TRANSMISSION = 20
    STATUS_TRANSACTION_DECLINED = 21
    STATUS_UNDEFINED_ERROR = 99
    ENCRYPT_PADDING = "PKCS1_v1_5" # OPENSSL_PKCS1_PADDING 
    SDK_VERSION = '1.2.0'

    def __init__(_self):
        pass
