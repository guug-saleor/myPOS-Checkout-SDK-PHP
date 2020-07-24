<?php

namespace Mypos\IPC;

/**
 * Container for SDK constants
 */
class Defines
{
    const COMMUNICATION_FORMAT_XML = 'xml';
    const COMMUNICATION_FORMAT_JSON = 'json';
    const COMMUNICATION_FORMAT_POST = 'post';
    const SIGNATURE_ALGO = OPENSSL_ALGO_SHA256;
    const STATUS_SUCCESS = 0;
    const STATUS_MISSING_REQ_PARAMS = 1;
    const STATUS_SIGNATURE_FAILED = 2;
    const STATUS_IPC_ERROR = 3;
    const STATUS_INVALID_SID = 4;
    const STATUS_INVALID_PARAMS = 5;
    const STATUS_INVALID_REFERER = 6;
    const STATUS_PAYMENT_TRIES = 7;
    const STATUS_TRANSACTION_AUTH_FAIL = 8;
    const STATUS_WRONG_AMOUNT = 9;
    const STATUS_UNSUPPORTED_CALL = 10;
    const STATUS_INACTIVE_MANDATE_REFERENCE = 11;
    const STATUS_INVALID_MANDATE_REFERENCE = 12;
    const STATUS_NOT_SUFFICIENT_FUNDS = 13;
    const STATUS_TRANSACTION_NOT_PERMITTED = 14;
    const STATUS_EXCEEDED_LIMIT = 15;
    const STATUS_MANDATE_ALREADY_REGISTERED = 16;
    const STATUS_INACTIVE_ACOUNTIDENTIFIER = 17;
    const STATUS_INVALID_ACOUNTIDENTIFIER = 18;
    const STATUS_EXCEEDED_ACCOUNT_LIMITS = 19;
    const STATUS_DUPLICATE_TRANSMISSION = 20;
    const STATUS_TRANSACTION_DECLINED = 21;
    const STATUS_UNDEFINED_ERROR = 99;
    const ENCRYPT_PADDING = OPENSSL_PKCS1_PADDING;
    const SDK_VERSION = '1.1.2';

    private function __construct() { }
}
