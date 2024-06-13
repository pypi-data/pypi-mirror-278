"""Module for getting Peach Payments result codes."""

from typing import Dict

from peachpayments_partner.exceptions import ResultCodeException


class ResultCode:
    """Represents a single result code.

    Attributes:
        - code (str): code representing the result
        - name (str): camelCase name of the result
        - description (str): detailed description of the result
    """

    def __init__(self, code: str, name: str, description: str = None):
        """Construct all the attributes for the ResultCode object.

        Args:
            - code (str): code representing the result
            - name (str): camelCase name of the result

        Kwargs:
            - description (str): detailed description of the result

        Raises:
            ResultCodeException if result code name or number is not provided.
        """
        if not code:
            raise ResultCodeException("Result code number not provided")

        if not name:
            raise ResultCodeException("Result code name not provided")

        self.code = code
        self.name = name
        self.description = description


class ResultCodes:
    """Collection of ResultCodes.

    Usage:
        result_codes.TRANSACTION_SUCCEEDED.code == "000.000.000"
        result_codes.get("000.000.000").name == "TRANSACTION_SUCCEEDED"
        result_codes.get("000.000.000").description == "Transaction succeeded"

    Attributes:
        - [ResultCode.name] (ResultCode)
        - by_code (dict) ResultCodes indexed by code number
    """

    by_code: Dict[str, ResultCode] = {}

    TRANSACTION_SUCCEEDED = ResultCode(
        code="000.000.000", name="TRANSACTION_SUCCEEDED", description="Transaction succeeded"
    )
    SUCCESSFUL_REQUEST = ResultCode(code="000.000.100", name="SUCCESSFUL_REQUEST", description="successful request")
    CHARGEBACK_REPRESENTMENT_IS_SUCCESSFUL = ResultCode(
        code="000.100.105",
        name="CHARGEBACK_REPRESENTMENT_IS_SUCCESSFUL",
        description="Chargeback Representment is successful",
    )
    CHARGEBACK_REPRESENTMENT_CANCELLATION_IS_SUCCESSFUL = ResultCode(
        code="000.100.106",
        name="CHARGEBACK_REPRESENTMENT_CANCELLATION_IS_SUCCESSFUL",
        description="Chargeback Representment cancellation is successful",
    )
    REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_INTEGRATOR_TEST_MODE = ResultCode(
        code="000.100.110",
        name="REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_INTEGRATOR_TEST_MODE",
        description="Request successfully processed in 'Merchant in Integrator Test Mode'",
    )
    REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_VALIDATOR_TEST_MODE = ResultCode(
        code="000.100.111",
        name="REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_VALIDATOR_TEST_MODE",
        description="Request successfully processed in 'Merchant in Validator Test Mode'",
    )
    REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_CONNECTOR_TEST_MODE = ResultCode(
        code="000.100.112",
        name="REQUEST_SUCCESSFULLY_PROCESSED_IN_MERCHANT_IN_CONNECTOR_TEST_MODE",
        description="Request successfully processed in 'Merchant in Connector Test Mode'",
    )
    REASON_NOT_SPECIFIED = ResultCode(
        code="000.100.200", name="REASON_NOT_SPECIFIED", description="Reason not Specified"
    )
    ACCOUNT_OR_BANK_DETAILS_INCORRECT_1 = ResultCode(
        code="000.100.201", name="ACCOUNT_OR_BANK_DETAILS_INCORRECT_1", description="Account or Bank Details Incorrect"
    )
    ACCOUNT_CLOSED_1 = ResultCode(code="000.100.202", name="ACCOUNT_CLOSED_1", description="Account Closed")
    INSUFFICIENT_FUNDS_1 = ResultCode(code="000.100.203", name="INSUFFICIENT_FUNDS_1", description="Insufficient Funds")
    MANDATE_NOT_VALID = ResultCode(code="000.100.204", name="MANDATE_NOT_VALID", description="Mandate not Valid")
    MANDATE_CANCELLED = ResultCode(code="000.100.205", name="MANDATE_CANCELLED", description="Mandate Cancelled")
    REVOCATION_OR_DISPUTE = ResultCode(
        code="000.100.206", name="REVOCATION_OR_DISPUTE", description="Revocation or Dispute"
    )
    CANCELLATION_IN_CLEARING_NETWORK = ResultCode(
        code="000.100.207", name="CANCELLATION_IN_CLEARING_NETWORK", description="Cancellation in Clearing Network"
    )
    ACCOUNT_BLOCKED = ResultCode(code="000.100.208", name="ACCOUNT_BLOCKED", description="Account Blocked")
    ACCOUNT_DOES_NOT_EXIST = ResultCode(
        code="000.100.209", name="ACCOUNT_DOES_NOT_EXIST", description="Account does not exist"
    )
    INVALID_AMOUNT = ResultCode(code="000.100.210", name="INVALID_AMOUNT", description="Invalid Amount")
    TRANSACTION_SUCCEEDED_AMOUNT_OF_TRANSACTION_IS_SMALLER_THEN_AMOUNT_OF_PREAUTHORIZATION = ResultCode(
        code="000.100.211",
        name="TRANSACTION_SUCCEEDED_AMOUNT_OF_TRANSACTION_IS_SMALLER_THEN_AMOUNT_OF_PREAUTHORIZATION",
        description="Transaction succeeded (amount of transaction is smaller then amount of pre-authorization)",
    )
    TRANSACTION_SUCCEEDED_AMOUNT_OF_TRANSACTION_IS_GREATER_THEN_AMOUNT_OF_PREAUTHORIZATION = ResultCode(
        code="000.100.212",
        name="TRANSACTION_SUCCEEDED_AMOUNT_OF_TRANSACTION_IS_GREATER_THEN_AMOUNT_OF_PREAUTHORIZATION",
        description="Transaction succeeded (amount of transaction is greater then amount of pre-authorization)",
    )
    FRAUDULENT_TRANSACTION = ResultCode(
        code="000.100.220", name="FRAUDULENT_TRANSACTION", description="Fraudulent Transaction"
    )
    MERCHANDISE_NOT_RECEIVED = ResultCode(
        code="000.100.221", name="MERCHANDISE_NOT_RECEIVED", description="Merchandise Not Received"
    )
    TRANSACTION_NOT_RECOGNIZED_BY_CARDHOLDER = ResultCode(
        code="000.100.222",
        name="TRANSACTION_NOT_RECOGNIZED_BY_CARDHOLDER",
        description="Transaction Not Recognized By Cardholder",
    )
    SERVICE_NOT_RENDERED = ResultCode(
        code="000.100.223", name="SERVICE_NOT_RENDERED", description="Service Not Rendered"
    )
    DUPLICATE_PROCESSING = ResultCode(
        code="000.100.224", name="DUPLICATE_PROCESSING", description="Duplicate Processing"
    )
    CREDIT_NOT_PROCESSED = ResultCode(
        code="000.100.225", name="CREDIT_NOT_PROCESSED", description="Credit Not Processed"
    )
    CANNOT_BE_SETTLED = ResultCode(code="000.100.226", name="CANNOT_BE_SETTLED", description="Cannot be settled")
    CONFIGURATION_ISSUE = ResultCode(code="000.100.227", name="CONFIGURATION_ISSUE", description="Configuration Issue")
    TEMPORARY_COMMUNICATION_ERROR__RETRY = ResultCode(
        code="000.100.228",
        name="TEMPORARY_COMMUNICATION_ERROR__RETRY",
        description="Temporary Communication Error - Retry",
    )
    INCORRECT_INSTRUCTIONS = ResultCode(
        code="000.100.229", name="INCORRECT_INSTRUCTIONS", description="Incorrect Instructions"
    )
    UNAUTHORISED_CHARGE = ResultCode(code="000.100.230", name="UNAUTHORISED_CHARGE", description="Unauthorised Charge")
    LATE_REPRESENTMENT = ResultCode(code="000.100.231", name="LATE_REPRESENTMENT", description="Late Representment")
    LIABILITY_SHIFT = ResultCode(code="000.100.232", name="LIABILITY_SHIFT", description="Liability Shift")
    AUTHORIZATION_RELATED_CHARGEBACK = ResultCode(
        code="000.100.233", name="AUTHORIZATION_RELATED_CHARGEBACK", description="Authorization-Related Chargeback"
    )
    NON_RECEIPT_OF_MERCHANDISE = ResultCode(
        code="000.100.234", name="NON_RECEIPT_OF_MERCHANDISE", description="Non receipt of merchandise"
    )
    UNSPECIFIED_TECHNICAL = ResultCode(
        code="000.100.299", name="UNSPECIFIED_TECHNICAL", description="Unspecified (Technical)"
    )
    TRANSACTION_PENDING = ResultCode(code="000.200.000", name="TRANSACTION_PENDING", description="transaction pending")
    TRANSACTION_PENDING_FOR_ACQUIRER_THE_CONSUMER_IS_NOT_PRESENT = ResultCode(
        code="000.200.001",
        name="TRANSACTION_PENDING_FOR_ACQUIRER_THE_CONSUMER_IS_NOT_PRESENT",
        description="Transaction pending for acquirer, the consumer is not present",
    )
    SUCCESSFULLY_CREATED_CHECKOUT = ResultCode(
        code="000.200.100", name="SUCCESSFULLY_CREATED_CHECKOUT", description="successfully created checkout"
    )
    SUCCESSFULLY_UPDATED_CHECKOUT = ResultCode(
        code="000.200.101", name="SUCCESSFULLY_UPDATED_CHECKOUT", description="successfully updated checkout"
    )
    SUCCESSFULLY_DELETED_CHECKOUT = ResultCode(
        code="000.200.102", name="SUCCESSFULLY_DELETED_CHECKOUT", description="successfully deleted checkout"
    )
    CHECKOUT_IS_PENDING = ResultCode(code="000.200.103", name="CHECKOUT_IS_PENDING", description="checkout is pending")
    TRANSACTION_INITIALIZED = ResultCode(
        code="000.200.200", name="TRANSACTION_INITIALIZED", description="Transaction initialized"
    )
    QR_SCANNED_LINK_CLICKED_WAITING_FOR_THE_FINAL_AUTHENTICATION_RESULT = ResultCode(
        code="000.200.201",
        name="QR_SCANNED_LINK_CLICKED_WAITING_FOR_THE_FINAL_AUTHENTICATION_RESULT",
        description="QR Scanned/Link Clicked, waiting for the final authentication result",
    )
    TWO_STEP_TRANSACTION_SUCCEEDED = ResultCode(
        code="000.300.000", name="TWO_STEP_TRANSACTION_SUCCEEDED", description="Two-step transaction succeeded"
    )
    RISK_CHECK_SUCCESSFUL = ResultCode(
        code="000.300.100", name="RISK_CHECK_SUCCESSFUL", description="Risk check successful"
    )
    RISK_BANK_ACCOUNT_CHECK_SUCCESSFUL = ResultCode(
        code="000.300.101", name="RISK_BANK_ACCOUNT_CHECK_SUCCESSFUL", description="Risk bank account check successful"
    )
    RISK_REPORT_SUCCESSFUL = ResultCode(
        code="000.300.102", name="RISK_REPORT_SUCCESSFUL", description="Risk report successful"
    )
    EXEMPTION_CHECK_SUCCESSFUL = ResultCode(
        code="000.300.103", name="EXEMPTION_CHECK_SUCCESSFUL", description="Exemption check successful"
    )
    ACCOUNT_UPDATED = ResultCode(code="000.310.100", name="ACCOUNT_UPDATED", description="Account updated")
    ACCOUNT_UPDATED_CREDIT_CARD_EXPIRED = ResultCode(
        code="000.310.101",
        name="ACCOUNT_UPDATED_CREDIT_CARD_EXPIRED",
        description="Account updated (Credit card expired)",
    )
    NO_UPDATES_FOUND_BUT_ACCOUNT_IS_VALID = ResultCode(
        code="000.310.110",
        name="NO_UPDATES_FOUND_BUT_ACCOUNT_IS_VALID",
        description="No updates found, but account is valid",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_FRAUD_SUSPICION = ResultCode(
        code="000.400.000",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_FRAUD_SUSPICION",
        description="Transaction succeeded (please review manually due to fraud suspicion)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_AVS_RETURN_CODE = ResultCode(
        code="000.400.010",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_AVS_RETURN_CODE",
        description="Transaction succeeded (please review manually due to AVS return code)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_CVV_RETURN_CODE = ResultCode(
        code="000.400.020",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_CVV_RETURN_CODE",
        description="Transaction succeeded (please review manually due to CVV return code)",
    )
    TRANSACTION_PARTIALLY_FAILED_PLEASE_REVERSE_MANUALLY_DUE_TO_FAILED_AUTOMATIC_REVERSAL = ResultCode(
        code="000.400.030",
        name="TRANSACTION_PARTIALLY_FAILED_PLEASE_REVERSE_MANUALLY_DUE_TO_FAILED_AUTOMATIC_REVERSAL",
        description="Transaction partially failed (please reverse manually due to failed automatic reversal)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_AMOUNT_MISMATCH = ResultCode(
        code="000.400.040",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_AMOUNT_MISMATCH",
        description="Transaction succeeded (please review manually due to amount mismatch)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_BECAUSE_TRANSACTION_IS_PENDING = ResultCode(
        code="000.400.050",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_BECAUSE_TRANSACTION_IS_PENDING",
        description="Transaction succeeded (please review manually because transaction is pending)",
    )
    TRANSACTION_SUCCEEDED_APPROVED_AT_MERCHANTS_RISK = ResultCode(
        code="000.400.060",
        name="TRANSACTION_SUCCEEDED_APPROVED_AT_MERCHANTS_RISK",
        description="Transaction succeeded (approved at merchant's risk)",
    )
    TRANSACTION_SUCCEEDED_WAITING_FOR_EXTERNAL_RISK_REVIEW = ResultCode(
        code="000.400.070",
        name="TRANSACTION_SUCCEEDED_WAITING_FOR_EXTERNAL_RISK_REVIEW",
        description="Transaction succeeded (waiting for external risk review)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_BECAUSE_THE_SERVICE_WAS_UNAVAILABLE = ResultCode(
        code="000.400.080",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_BECAUSE_THE_SERVICE_WAS_UNAVAILABLE",
        description="Transaction succeeded (please review manually because the service was unavailable)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_AS_THE_RISK_STATUS_NOT_AVAILABLE_YET_DUE_NETWORK_TIMEOUT = ResultCode(
        code="000.400.081",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_AS_THE_RISK_STATUS_NOT_AVAILABLE_YET_DUE_NETWORK_TIMEOUT",
        description="Transaction succeeded (please review manually, "
        "as the risk status not available yet due network timeout)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_AS_THE_RISK_STATUS_NOT_AVAILABLE_YET_DUE_PROCESSING_TIMEOUT = ResultCode(  # noqa: E501
        code="000.400.082",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_AS_THE_RISK_STATUS_NOT_AVAILABLE_YET_DUE_PROCESSING_TIMEOUT",
        description="Transaction succeeded (please review manually, "
        "as the risk status not available yet due processing timeout)",
    )
    TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_EXTERNAL_RISK_CHECK = ResultCode(
        code="000.400.090",
        name="TRANSACTION_SUCCEEDED_PLEASE_REVIEW_MANUALLY_DUE_TO_EXTERNAL_RISK_CHECK",
        description="Transaction succeeded (please review manually due to external risk check)",
    )
    TRANSACTION_SUCCEEDED_RISK_AFTER_PAYMENT_REJECTED = ResultCode(
        code="000.400.100",
        name="TRANSACTION_SUCCEEDED_RISK_AFTER_PAYMENT_REJECTED",
        description="Transaction succeeded, risk after payment rejected",
    )
    CARD_NOT_PARTICIPATING_AUTHENTICATION_UNAVAILABLE = ResultCode(
        code="000.400.101",
        name="CARD_NOT_PARTICIPATING_AUTHENTICATION_UNAVAILABLE",
        description="card not participating/authentication unavailable",
    )
    USER_NOT_ENROLLED = ResultCode(code="000.400.102", name="USER_NOT_ENROLLED", description="user not enrolled")
    TECHNICAL_ERROR_IN_3D_SYSTEM_1 = ResultCode(
        code="000.400.103", name="TECHNICAL_ERROR_IN_3D_SYSTEM_1", description="Technical Error in 3D system"
    )
    MISSING_OR_MALFORMED_3DSECURE_CONFIGURATION_FOR_CHANNEL = ResultCode(
        code="000.400.104",
        name="MISSING_OR_MALFORMED_3DSECURE_CONFIGURATION_FOR_CHANNEL",
        description="Missing or malformed 3DSecure Configuration for Channel",
    )
    UNSUPPORTED_USER_DEVICE__AUTHENTICATION_NOT_POSSIBLE_1 = ResultCode(
        code="000.400.105",
        name="UNSUPPORTED_USER_DEVICE__AUTHENTICATION_NOT_POSSIBLE_1",
        description="Unsupported User Device - Authentication not possible",
    )
    INVALID_PAYER_AUTHENTICATION_RESPONSE_PARES_IN_3DSECURE_TRANSACTION = ResultCode(
        code="000.400.106",
        name="INVALID_PAYER_AUTHENTICATION_RESPONSE_PARES_IN_3DSECURE_TRANSACTION",
        description="invalid payer authentication response(PARes) in 3DSecure Transaction",
    )
    COMMUNICATION_ERROR_TO_SCHEME_DIRECTORY_SERVER_1 = ResultCode(
        code="000.400.107",
        name="COMMUNICATION_ERROR_TO_SCHEME_DIRECTORY_SERVER_1",
        description="Communication Error to Scheme Directory Server",
    )
    CARDHOLDER_NOT_FOUND__CARD_NUMBER_PROVIDED_IS_NOT_FOUND_IN_THE_RANGES_OF_THE_ISSUER_1 = ResultCode(
        code="000.400.108",
        name="CARDHOLDER_NOT_FOUND__CARD_NUMBER_PROVIDED_IS_NOT_FOUND_IN_THE_RANGES_OF_THE_ISSUER_1",
        description="Cardholder Not Found - card number provided is not found in the ranges of the issuer",
    )
    CARD_IS_NOT_ENROLLED_FOR_3DS_VERSION_2 = ResultCode(
        code="000.400.109",
        name="CARD_IS_NOT_ENROLLED_FOR_3DS_VERSION_2",
        description="Card is not enrolled for 3DS version 2",
    )
    AUTHENTICATION_SUCCESSFUL_FRICTIONLESS_FLOW = ResultCode(
        code="000.400.110",
        name="AUTHENTICATION_SUCCESSFUL_FRICTIONLESS_FLOW",
        description="Authentication successful (frictionless flow)",
    )
    DATA_ONLY_REQUEST_FAILED = ResultCode(
        code="000.400.111", name="DATA_ONLY_REQUEST_FAILED", description="Data Only request failed"
    )
    AUTHENTICATION_SUCCESSFUL_DATA_ONLY_FLOW = ResultCode(
        code="000.400.120",
        name="AUTHENTICATION_SUCCESSFUL_DATA_ONLY_FLOW",
        description="Authentication successful (data only flow)",
    )
    RISK_MANAGEMENT_CHECK_COMMUNICATION_ERROR = ResultCode(
        code="000.400.200",
        name="RISK_MANAGEMENT_CHECK_COMMUNICATION_ERROR",
        description="risk management check communication error",
    )
    TRANSACTION_SUCCEEDED__VERY_GOOD_RATING = ResultCode(
        code="000.500.000",
        name="TRANSACTION_SUCCEEDED__VERY_GOOD_RATING",
        description="Transaction succeeded - very good rating",
    )
    TRANSACTION_SUCCEEDED_ADDRESS_CORRECTED = ResultCode(
        code="000.500.100",
        name="TRANSACTION_SUCCEEDED_ADDRESS_CORRECTED",
        description="Transaction succeeded (address corrected)",
    )
    TRANSACTION_SUCCEEDED_DUE_TO_EXTERNAL_UPDATE = ResultCode(
        code="000.600.000",
        name="TRANSACTION_SUCCEEDED_DUE_TO_EXTERNAL_UPDATE",
        description="transaction succeeded due to external update",
    )
    REQUEST_CONTAINS_NO_CREDITCARD_BANK_ACCOUNT_NUMBER_OR_BANK_NAME = ResultCode(
        code="100.100.100",
        name="REQUEST_CONTAINS_NO_CREDITCARD_BANK_ACCOUNT_NUMBER_OR_BANK_NAME",
        description="request contains no creditcard, bank account number or bank name",
    )
    INVALID_CREDITCARD_BANK_ACCOUNT_NUMBER_OR_BANK_NAME = ResultCode(
        code="100.100.101",
        name="INVALID_CREDITCARD_BANK_ACCOUNT_NUMBER_OR_BANK_NAME",
        description="invalid creditcard, bank account number or bank name",
    )
    INVALID_UNIQUE_ID__ROOT_UNIQUE_ID = ResultCode(
        code="100.100.104", name="INVALID_UNIQUE_ID__ROOT_UNIQUE_ID", description="invalid unique id / root unique id"
    )
    REQUEST_CONTAINS_NO_MONTH = ResultCode(
        code="100.100.200", name="REQUEST_CONTAINS_NO_MONTH", description="request contains no month"
    )
    INVALID_MONTH = ResultCode(code="100.100.201", name="INVALID_MONTH", description="invalid month")
    REQUEST_CONTAINS_NO_YEAR = ResultCode(
        code="100.100.300", name="REQUEST_CONTAINS_NO_YEAR", description="request contains no year"
    )
    INVALID_YEAR = ResultCode(code="100.100.301", name="INVALID_YEAR", description="invalid year")
    CARD_EXPIRED = ResultCode(code="100.100.303", name="CARD_EXPIRED", description="card expired")
    CARD_NOT_YET_VALID = ResultCode(code="100.100.304", name="CARD_NOT_YET_VALID", description="card not yet valid")
    INVALID_EXPIRATION_DATE_FORMAT = ResultCode(
        code="100.100.305", name="INVALID_EXPIRATION_DATE_FORMAT", description="invalid expiration date format"
    )
    REQUEST_CONTAINS_NO_CC_BANK_ACCOUNT_HOLDER = ResultCode(
        code="100.100.400",
        name="REQUEST_CONTAINS_NO_CC_BANK_ACCOUNT_HOLDER",
        description="request contains no cc/bank account holder",
    )
    CC_BANK_ACCOUNT_HOLDER_TOO_SHORT_OR_TOO_LONG = ResultCode(
        code="100.100.401",
        name="CC_BANK_ACCOUNT_HOLDER_TOO_SHORT_OR_TOO_LONG",
        description="cc/bank account holder too short or too long",
    )
    CC_BANK_ACCOUNT_HOLDER_NOT_VALID_1 = ResultCode(
        code="100.100.402", name="CC_BANK_ACCOUNT_HOLDER_NOT_VALID_1", description="cc/bank account holder not valid"
    )
    REQUEST_CONTAINS_NO_CREDIT_CARD_BRAND = ResultCode(
        code="100.100.500",
        name="REQUEST_CONTAINS_NO_CREDIT_CARD_BRAND",
        description="request contains no credit card brand",
    )
    INVALID_CREDIT_CARD_BRAND = ResultCode(
        code="100.100.501", name="INVALID_CREDIT_CARD_BRAND", description="invalid credit card brand"
    )
    EMPTY_CVV_FOR_VISA_MASTER_AMEX_NOT_ALLOWED = ResultCode(
        code="100.100.600",
        name="EMPTY_CVV_FOR_VISA_MASTER_AMEX_NOT_ALLOWED",
        description="empty CVV for VISA,MASTER, AMEX not allowed",
    )
    INVALID_CVV_BRAND_COMBINATION = ResultCode(
        code="100.100.601", name="INVALID_CVV_BRAND_COMBINATION", description="invalid CVV/brand combination"
    )
    EMPTY_CREDITCARDISSUENUMBER_FOR_MAESTRO_NOT_ALLOWED = ResultCode(
        code="100.100.650",
        name="EMPTY_CREDITCARDISSUENUMBER_FOR_MAESTRO_NOT_ALLOWED",
        description="empty CreditCardIssueNumber for MAESTRO not allowed",
    )
    INVALID_CREDITCARDISSUENUMBER = ResultCode(
        code="100.100.651", name="INVALID_CREDITCARDISSUENUMBER", description="invalid CreditCardIssueNumber"
    )
    INVALID_CC_NUMBER_BRAND_COMBINATION = ResultCode(
        code="100.100.700",
        name="INVALID_CC_NUMBER_BRAND_COMBINATION",
        description="invalid cc number/brand combination",
    )
    SUSPECTING_FRAUD_THIS_CARD_MAY_NOT_BE_PROCESSED = ResultCode(
        code="100.100.701",
        name="SUSPECTING_FRAUD_THIS_CARD_MAY_NOT_BE_PROCESSED",
        description="suspecting fraud, this card may not be processed",
    )
    REQUEST_CONTAINS_NO_ACCOUNT_DATA_AND_NO_REGISTRATION_ID = ResultCode(
        code="100.150.100",
        name="REQUEST_CONTAINS_NO_ACCOUNT_DATA_AND_NO_REGISTRATION_ID",
        description="request contains no Account data and no registration id",
    )
    INVALID_FORMAT_FOR_SPECIFIED_REGISTRATION_ID_MUST_BE_UUID_FORMAT = ResultCode(
        code="100.150.101",
        name="INVALID_FORMAT_FOR_SPECIFIED_REGISTRATION_ID_MUST_BE_UUID_FORMAT",
        description="invalid format for specified registration id (must be uuid format)",
    )
    REGISTRATION_DOES_NOT_EXIST = ResultCode(
        code="100.150.200", name="REGISTRATION_DOES_NOT_EXIST", description="registration does not exist"
    )
    REGISTRATION_IS_NOT_CONFIRMED_YET = ResultCode(
        code="100.150.201", name="REGISTRATION_IS_NOT_CONFIRMED_YET", description="registration is not confirmed yet"
    )
    REGISTRATION_IS_ALREADY_DEREGISTERED = ResultCode(
        code="100.150.202",
        name="REGISTRATION_IS_ALREADY_DEREGISTERED",
        description="registration is already deregistered",
    )
    REGISTRATION_IS_NOT_VALID_PROBABLY_INITIALLY_REJECTED = ResultCode(
        code="100.150.203",
        name="REGISTRATION_IS_NOT_VALID_PROBABLY_INITIALLY_REJECTED",
        description="registration is not valid, probably initially rejected",
    )
    ACCOUNT_REGISTRATION_REFERENCE_POINTED_TO_NO_REGISTRATION_TRANSACTION = ResultCode(
        code="100.150.204",
        name="ACCOUNT_REGISTRATION_REFERENCE_POINTED_TO_NO_REGISTRATION_TRANSACTION",
        description="account registration reference pointed to no registration transaction",
    )
    REFERENCED_REGISTRATION_DOES_NOT_CONTAIN_AN_ACCOUNT = ResultCode(
        code="100.150.205",
        name="REFERENCED_REGISTRATION_DOES_NOT_CONTAIN_AN_ACCOUNT",
        description="referenced registration does not contain an account",
    )
    PAYMENT_ONLY_ALLOWED_WITH_VALID_INITIAL_REGISTRATION = ResultCode(
        code="100.150.300",
        name="PAYMENT_ONLY_ALLOWED_WITH_VALID_INITIAL_REGISTRATION",
        description="payment only allowed with valid initial registration",
    )
    BANK_ACCOUNT_CONTAINS_NO_OR_INVALID_COUNTRY = ResultCode(
        code="100.200.100",
        name="BANK_ACCOUNT_CONTAINS_NO_OR_INVALID_COUNTRY",
        description="bank account contains no or invalid country",
    )
    BANK_ACCOUNT_HAS_INVALID_BANKCODE_NAME_ACCOUNT_NUMBER_COMBINATION = ResultCode(
        code="100.200.103",
        name="BANK_ACCOUNT_HAS_INVALID_BANKCODE_NAME_ACCOUNT_NUMBER_COMBINATION",
        description="bank account has invalid bankcode/name account number combination",
    )
    BANK_ACCOUNT_HAS_INVALID_ACCCOUNT_NUMBER_FORMAT = ResultCode(
        code="100.200.104",
        name="BANK_ACCOUNT_HAS_INVALID_ACCCOUNT_NUMBER_FORMAT",
        description="bank account has invalid acccount number format",
    )
    BANK_ACCOUNT_NEEDS_TO_BE_REGISTERED_AND_CONFIRMED_FIRST_COUNTRY_IS_MANDATE_BASED = ResultCode(
        code="100.200.200",
        name="BANK_ACCOUNT_NEEDS_TO_BE_REGISTERED_AND_CONFIRMED_FIRST_COUNTRY_IS_MANDATE_BASED",
        description="bank account needs to be registered and confirmed first. Country is mandate based.",
    )
    VIRTUAL_ACCOUNT_CONTAINS_NO_OR_INVALID_ID = ResultCode(
        code="100.210.101",
        name="VIRTUAL_ACCOUNT_CONTAINS_NO_OR_INVALID_ID",
        description="virtual account contains no or invalid Id",
    )
    VIRTUAL_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND = ResultCode(
        code="100.210.102",
        name="VIRTUAL_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND",
        description="virtual account contains no or invalid brand",
    )
    USER_ACCOUNT_CONTAINS_NO_OR_INVALID_ID = ResultCode(
        code="100.211.101",
        name="USER_ACCOUNT_CONTAINS_NO_OR_INVALID_ID",
        description="user account contains no or invalid Id",
    )
    USER_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND = ResultCode(
        code="100.211.102",
        name="USER_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND",
        description="user account contains no or invalid brand",
    )
    NO_PASSWORD_DEFINED_FOR_USER_ACCOUNT = ResultCode(
        code="100.211.103",
        name="NO_PASSWORD_DEFINED_FOR_USER_ACCOUNT",
        description="no password defined for user account",
    )
    PASSWORD_DOES_NOT_MEET_SAFETY_REQUIREMENTS_NEEDS_8_DIGITS_AT_LEAST_AND_MUST_CONTAIN_LETTERS_AND_NUMBERS = ResultCode(  # noqa: E501
        code="100.211.104",
        name="PASSWORD_DOES_NOT_MEET_SAFETY_REQUIREMENTS_NEEDS_8_DIGITS_AT_LEAST_AND_MUST_CONTAIN_LETTERS_AND_NUMBERS",
        description="password does not meet safety requirements "
        "(needs 8 digits at least and must contain letters and numbers)",
    )
    WALLET_ID_HAS_TO_BE_A_VALID_EMAIL_ADDRESS = ResultCode(
        code="100.211.105",
        name="WALLET_ID_HAS_TO_BE_A_VALID_EMAIL_ADDRESS",
        description="wallet id has to be a valid email address",
    )
    VOUCHER_IDS_HAVE_32_DIGITS_ALWAYS = ResultCode(
        code="100.211.106", name="VOUCHER_IDS_HAVE_32_DIGITS_ALWAYS", description="voucher ids have 32 digits always"
    )
    WALLET_ACCOUNT_REGISTRATION_MUST_NOT_HAVE_AN_INITIAL_BALANCE = ResultCode(
        code="100.212.101",
        name="WALLET_ACCOUNT_REGISTRATION_MUST_NOT_HAVE_AN_INITIAL_BALANCE",
        description="wallet account registration must not have an initial balance",
    )
    WALLET_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND = ResultCode(
        code="100.212.102",
        name="WALLET_ACCOUNT_CONTAINS_NO_OR_INVALID_BRAND",
        description="wallet account contains no or invalid brand",
    )
    WALLET_ACCOUNT_PAYMENT_TRANSACTION_NEEDS_TO_REFERENCE_A_REGISTRATION = ResultCode(
        code="100.212.103",
        name="WALLET_ACCOUNT_PAYMENT_TRANSACTION_NEEDS_TO_REFERENCE_A_REGISTRATION",
        description="wallet account payment transaction needs to reference a registration",
    )
    JOB_CONTAINS_NO_EXECUTION_INFORMATION = ResultCode(
        code="100.250.100",
        name="JOB_CONTAINS_NO_EXECUTION_INFORMATION",
        description="job contains no execution information",
    )
    INVALID_OR_MISSING_ACTION_TYPE = ResultCode(
        code="100.250.105", name="INVALID_OR_MISSING_ACTION_TYPE", description="invalid or missing action type"
    )
    INVALID_OR_MISSING_DURATION_UNIT = ResultCode(
        code="100.250.106", name="INVALID_OR_MISSING_DURATION_UNIT", description="invalid or missing duration unit"
    )
    INVALID_OR_MISSING_NOTICE_UNIT = ResultCode(
        code="100.250.107", name="INVALID_OR_MISSING_NOTICE_UNIT", description="invalid or missing notice unit"
    )
    MISSING_JOB_EXECUTION = ResultCode(
        code="100.250.110", name="MISSING_JOB_EXECUTION", description="missing job execution"
    )
    MISSING_JOB_EXPRESSION = ResultCode(
        code="100.250.111", name="MISSING_JOB_EXPRESSION", description="missing job expression"
    )
    INVALID_EXECUTION_PARAMETERS_COMBINATION_DOES_NOT_CONFORM_TO_STANDARD = ResultCode(
        code="100.250.120",
        name="INVALID_EXECUTION_PARAMETERS_COMBINATION_DOES_NOT_CONFORM_TO_STANDARD",
        description="invalid execution parameters, combination does not conform to standard",
    )
    INVALID_EXECUTION_PARAMETERS_HOUR_MUST_BE_BETWEEN_0_AND_23 = ResultCode(
        code="100.250.121",
        name="INVALID_EXECUTION_PARAMETERS_HOUR_MUST_BE_BETWEEN_0_AND_23",
        description="invalid execution parameters, hour must be between 0 and 23",
    )
    INVALID_EXECUTION_PARAMETERS_MINUTE_AND_SECONDS_MUST_BE_BETWEEN_0_AND_59 = ResultCode(
        code="100.250.122",
        name="INVALID_EXECUTION_PARAMETERS_MINUTE_AND_SECONDS_MUST_BE_BETWEEN_0_AND_59",
        description="invalid execution parameters, minute and seconds must be between 0 and 59",
    )
    INVALID_EXECUTION_PARAMETERS_DAY_OF_MONTH_MUST_BE_BETWEEN_1_AND_31 = ResultCode(
        code="100.250.123",
        name="INVALID_EXECUTION_PARAMETERS_DAY_OF_MONTH_MUST_BE_BETWEEN_1_AND_31",
        description="invalid execution parameters, Day of month must be between 1 and 31",
    )
    INVALID_EXECUTION_PARAMETERS_MONTH_MUST_BE_BETWEEN_1_AND_12 = ResultCode(
        code="100.250.124",
        name="INVALID_EXECUTION_PARAMETERS_MONTH_MUST_BE_BETWEEN_1_AND_12",
        description="invalid execution parameters, month must be between 1 and 12",
    )
    INVALID_EXECUTION_PARAMETERS_DAY_OF_WEEK_MUST_BE_BETWEEN_1_AND_7 = ResultCode(
        code="100.250.125",
        name="INVALID_EXECUTION_PARAMETERS_DAY_OF_WEEK_MUST_BE_BETWEEN_1_AND_7",
        description="invalid execution parameters, Day of week must be between 1 and 7",
    )
    JOB_TAG_MISSING = ResultCode(code="100.250.250", name="JOB_TAG_MISSING", description="Job tag missing")
    INVALID_TEST_MODE_PLEASE_USE_LIVE_OR_INTEGRATOR_TEST_OR_CONNECTOR_TEST = ResultCode(
        code="100.300.101",
        name="INVALID_TEST_MODE_PLEASE_USE_LIVE_OR_INTEGRATOR_TEST_OR_CONNECTOR_TEST",
        description="invalid test mode (please use LIVE or INTEGRATOR_TEST or CONNECTOR_TEST)",
    )
    TRANSACTION_ID_TOO_LONG = ResultCode(
        code="100.300.200", name="TRANSACTION_ID_TOO_LONG", description="transaction id too long"
    )
    INVALID_REFERENCE_ID = ResultCode(
        code="100.300.300", name="INVALID_REFERENCE_ID", description="invalid reference id"
    )
    MISSING_OR_INVALID_CHANNEL_ID = ResultCode(
        code="100.300.400", name="MISSING_OR_INVALID_CHANNEL_ID", description="missing or invalid channel id"
    )
    MISSING_OR_INVALID_SENDER_ID = ResultCode(
        code="100.300.401", name="MISSING_OR_INVALID_SENDER_ID", description="missing or invalid sender id"
    )
    MISSING_OR_INVALID_VERSION = ResultCode(
        code="100.300.402", name="MISSING_OR_INVALID_VERSION", description="missing or invalid version"
    )
    INVALID_RESPONSE_ID = ResultCode(code="100.300.501", name="INVALID_RESPONSE_ID", description="invalid response id")
    INVALID_OR_MISSING_USER_LOGIN = ResultCode(
        code="100.300.600", name="INVALID_OR_MISSING_USER_LOGIN", description="invalid or missing user login"
    )
    INVALID_OR_MISSING_USER_PWD = ResultCode(
        code="100.300.601", name="INVALID_OR_MISSING_USER_PWD", description="invalid or missing user pwd"
    )
    INVALID_RELEVANCE = ResultCode(code="100.300.700", name="INVALID_RELEVANCE", description="invalid relevance")
    INVALID_RELEVANCE_FOR_GIVEN_PAYMENT_TYPE = ResultCode(
        code="100.300.701",
        name="INVALID_RELEVANCE_FOR_GIVEN_PAYMENT_TYPE",
        description="invalid relevance for given payment type",
    )
    ACCOUNT_MANAGEMENT_TYPE_NOT_SUPPORTED = ResultCode(
        code="100.310.401",
        name="ACCOUNT_MANAGEMENT_TYPE_NOT_SUPPORTED",
        description="Account management type not supported",
    )
    ACCOUNT_MANAGEMENT_TRANSACTION_NOT_ALLOWED_IN_CURRENT_STATE = ResultCode(
        code="100.310.402",
        name="ACCOUNT_MANAGEMENT_TRANSACTION_NOT_ALLOWED_IN_CURRENT_STATE",
        description="Account management transaction not allowed in current state",
    )
    REFERENCED_SESSION_IS_REJECTED_NO_ACTION_POSSIBLE = ResultCode(
        code="100.350.100",
        name="REFERENCED_SESSION_IS_REJECTED_NO_ACTION_POSSIBLE",
        description="referenced session is REJECTED (no action possible).",
    )
    REFERENCED_SESSION_IS_CLOSED_NO_ACTION_POSSIBLE = ResultCode(
        code="100.350.101",
        name="REFERENCED_SESSION_IS_CLOSED_NO_ACTION_POSSIBLE",
        description="referenced session is CLOSED (no action possible)",
    )
    UNDEFINED_SESSION_STATE = ResultCode(
        code="100.350.200", name="UNDEFINED_SESSION_STATE", description="undefined session state"
    )
    REFERENCING_A_REGISTRATION_THROUGH_REFERENCE_ID_IS_NOT_APPLICABLE_FOR_THIS_PAYMENT_TYPE = ResultCode(
        code="100.350.201",
        name="REFERENCING_A_REGISTRATION_THROUGH_REFERENCE_ID_IS_NOT_APPLICABLE_FOR_THIS_PAYMENT_TYPE",
        description="referencing a registration through reference id is not applicable for this payment type",
    )
    CONFIRMATION_CF_MUST_BE_REGISTERED_RG_FIRST = ResultCode(
        code="100.350.301",
        name="CONFIRMATION_CF_MUST_BE_REGISTERED_RG_FIRST",
        description="confirmation (CF) must be registered (RG) first",
    )
    SESSION_ALREADY_CONFIRMED_CF = ResultCode(
        code="100.350.302", name="SESSION_ALREADY_CONFIRMED_CF", description="session already confirmed (CF)"
    )
    CANNOT_DEREGISTER_DR_UNREGISTERED_ACCOUNT_AND_OR_CUSTOMER = ResultCode(
        code="100.350.303",
        name="CANNOT_DEREGISTER_DR_UNREGISTERED_ACCOUNT_AND_OR_CUSTOMER",
        description="cannot deregister (DR) unregistered account and/or customer",
    )
    CANNOT_CONFIRM_CF_SESSION_VIA_XML = ResultCode(
        code="100.350.310", name="CANNOT_CONFIRM_CF_SESSION_VIA_XML", description="cannot confirm (CF) session via XML"
    )
    CANNOT_CONFIRM_CF_ON_A_REGISTRATION_PASSTHROUGH_CHANNEL = ResultCode(
        code="100.350.311",
        name="CANNOT_CONFIRM_CF_ON_A_REGISTRATION_PASSTHROUGH_CHANNEL",
        description="cannot confirm (CF) on a registration passthrough channel",
    )
    CANNOT_DO_PASSTHROUGH_ON_NON_INTERNAL_CONNECTOR = ResultCode(
        code="100.350.312",
        name="CANNOT_DO_PASSTHROUGH_ON_NON_INTERNAL_CONNECTOR",
        description="cannot do passthrough on non-internal connector",
    )
    REGISTRATION_OF_THIS_TYPE_HAS_TO_PROVIDE_CONFIRMATION_URL = ResultCode(
        code="100.350.313",
        name="REGISTRATION_OF_THIS_TYPE_HAS_TO_PROVIDE_CONFIRMATION_URL",
        description="registration of this type has to provide confirmation url",
    )
    CUSTOMER_COULD_NOT_BE_NOTIFIED_OF_PIN_TO_CONFIRM_REGISTRATION_CHANNEL = ResultCode(
        code="100.350.314",
        name="CUSTOMER_COULD_NOT_BE_NOTIFIED_OF_PIN_TO_CONFIRM_REGISTRATION_CHANNEL",
        description="customer could not be notified of pin to confirm registration (channel)",
    )
    CUSTOMER_COULD_NOT_BE_NOTIFIED_OF_PIN_TO_CONFIRM_REGISTRATION_SENDING_FAILED = ResultCode(
        code="100.350.315",
        name="CUSTOMER_COULD_NOT_BE_NOTIFIED_OF_PIN_TO_CONFIRM_REGISTRATION_SENDING_FAILED",
        description="customer could not be notified of pin to confirm registration (sending failed)",
    )
    CANNOT_EXTEND_THE_TOKEN_TE_ON_UNREGISTERED_ACCOUNT = ResultCode(
        code="100.350.316",
        name="CANNOT_EXTEND_THE_TOKEN_TE_ON_UNREGISTERED_ACCOUNT",
        description="cannot extend the token (TE) on unregistered account",
    )
    NO_OR_INVALID_PIN_EMAIL_SMS_MICRODEPOSIT_AUTHENTICATION_ENTERED = ResultCode(
        code="100.350.400",
        name="NO_OR_INVALID_PIN_EMAIL_SMS_MICRODEPOSIT_AUTHENTICATION_ENTERED",
        description="no or invalid PIN (email/SMS/MicroDeposit authentication) entered",
    )
    UNABLE_TO_OBTAIN_PERSONAL_VIRTUAL_ACCOUNT__MOST_LIKELY_NO_MORE_ACCOUNTS_AVAILABLE = ResultCode(
        code="100.350.500",
        name="UNABLE_TO_OBTAIN_PERSONAL_VIRTUAL_ACCOUNT__MOST_LIKELY_NO_MORE_ACCOUNTS_AVAILABLE",
        description="unable to obtain personal (virtual) account - most likely no more accounts available",
    )
    REGISTRATION_IS_NOT_ALLOWED_TO_REFERENCE_ANOTHER_TRANSACTION = ResultCode(
        code="100.350.601",
        name="REGISTRATION_IS_NOT_ALLOWED_TO_REFERENCE_ANOTHER_TRANSACTION",
        description="registration is not allowed to reference another transaction",
    )
    REGISTRATION_IS_NOT_ALLOWED_FOR_RECURRING_PAYMENT_MIGRATION = ResultCode(
        code="100.350.602",
        name="REGISTRATION_IS_NOT_ALLOWED_FOR_RECURRING_PAYMENT_MIGRATION",
        description="Registration is not allowed for recurring payment migration",
    )
    UNKNOWN_SCHEDULE_TYPE = ResultCode(
        code="100.360.201", name="UNKNOWN_SCHEDULE_TYPE", description="unknown schedule type"
    )
    CANNOT_SCHEDULE_SD_UNSCHEDULED_JOB = ResultCode(
        code="100.360.300", name="CANNOT_SCHEDULE_SD_UNSCHEDULED_JOB", description="cannot schedule(SD) unscheduled job"
    )
    CANNOT_DESCHEDULE_DS_UNSCHEDULED_JOB = ResultCode(
        code="100.360.303",
        name="CANNOT_DESCHEDULE_DS_UNSCHEDULED_JOB",
        description="cannot deschedule(DS) unscheduled job",
    )
    SCHEDULE_MODULE_NOT_CONFIGURED_FOR_LIVE_TRANSACTION_MODE = ResultCode(
        code="100.360.400",
        name="SCHEDULE_MODULE_NOT_CONFIGURED_FOR_LIVE_TRANSACTION_MODE",
        description="schedule module not configured for LIVE transaction mode",
    )
    TRANSACTION_DECLINED_1 = ResultCode(
        code="100.370.100", name="TRANSACTION_DECLINED_1", description="transaction declined"
    )
    RESPONSEURL_NOT_SET_IN_TRANSACTION_FRONTEND = ResultCode(
        code="100.370.101",
        name="RESPONSEURL_NOT_SET_IN_TRANSACTION_FRONTEND",
        description="responseUrl not set in Transaction/Frontend",
    )
    MALFORMED_RESPONSEURL_IN_TRANSACTION_FRONTEND = ResultCode(
        code="100.370.102",
        name="MALFORMED_RESPONSEURL_IN_TRANSACTION_FRONTEND",
        description="malformed responseUrl in Transaction/Frontend",
    )
    TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_1 = ResultCode(
        code="100.370.110",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_1",
        description="transaction must be executed for German address",
    )
    SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_1 = ResultCode(
        code="100.370.111",
        name="SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_1",
        description="system error( possible incorrect/missing input data)",
    )
    NO_OR_UNKNOWN_ECI_TYPE_DEFINED_IN_AUTHENTICATION = ResultCode(
        code="100.370.121",
        name="NO_OR_UNKNOWN_ECI_TYPE_DEFINED_IN_AUTHENTICATION",
        description="no or unknown ECI Type defined in Authentication",
    )
    PARAMETER_WITH_NULL_KEY_PROVIDED_IN_3DSECURE_AUTHENTICATION = ResultCode(
        code="100.370.122",
        name="PARAMETER_WITH_NULL_KEY_PROVIDED_IN_3DSECURE_AUTHENTICATION",
        description="parameter with null key provided in 3DSecure Authentication",
    )
    NO_OR_UNKNOWN_VERIFICATION_TYPE_DEFINED_IN_3DSECURE_AUTHENTICATION = ResultCode(
        code="100.370.123",
        name="NO_OR_UNKNOWN_VERIFICATION_TYPE_DEFINED_IN_3DSECURE_AUTHENTICATION",
        description="no or unknown verification type defined in 3DSecure Authentication",
    )
    UNKNOWN_PARAMETER_KEY_IN_3DSECURE_AUTHENTICATION = ResultCode(
        code="100.370.124",
        name="UNKNOWN_PARAMETER_KEY_IN_3DSECURE_AUTHENTICATION",
        description="unknown parameter key in 3DSecure Authentication",
    )
    INVALID_3DSECURE_VERIFICATION_ID_MUST_HAVE_BASE64_ENCODING_A_LENGTH_OF_28_DIGITS = ResultCode(
        code="100.370.125",
        name="INVALID_3DSECURE_VERIFICATION_ID_MUST_HAVE_BASE64_ENCODING_A_LENGTH_OF_28_DIGITS",
        description="Invalid 3DSecure Verification_ID. Must have Base64 encoding a Length of 28 digits",
    )
    NO_OR_UNKNOWN_AUTHENTICATION_TYPE_DEFINED_IN_TRANSACTION_AUTHENTICATIONTYPE = ResultCode(
        code="100.370.131",
        name="NO_OR_UNKNOWN_AUTHENTICATION_TYPE_DEFINED_IN_TRANSACTION_AUTHENTICATIONTYPE",
        description="no or unknown authentication type defined in Transaction/Authentication@type",
    )
    NO_RESULT_INDICATOR_DEFINED_TRANSACTION_AUTHENTICATION_RESULTINDICATOR = ResultCode(
        code="100.370.132",
        name="NO_RESULT_INDICATOR_DEFINED_TRANSACTION_AUTHENTICATION_RESULTINDICATOR",
        description="no result indicator defined Transaction/Authentication/resultIndicator",
    )
    TRANSACTION_DECLINED_2 = ResultCode(
        code="100.380.100", name="TRANSACTION_DECLINED_2", description="transaction declined"
    )
    TRANSACTION_CONTAINS_NO_RISK_MANAGEMENT_PART = ResultCode(
        code="100.380.101",
        name="TRANSACTION_CONTAINS_NO_RISK_MANAGEMENT_PART",
        description="transaction contains no risk management part",
    )
    TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_2 = ResultCode(
        code="100.380.110",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_2",
        description="transaction must be executed for German address",
    )
    NO_RISK_MANAGEMENT_PROCESS_TYPE_SPECIFIED = ResultCode(
        code="100.380.201",
        name="NO_RISK_MANAGEMENT_PROCESS_TYPE_SPECIFIED",
        description="no risk management process type specified",
    )
    NO_FRONTEND_INFORMATION_PROVIDED_FOR_ASYNCHRONOUS_TRANSACTION = ResultCode(
        code="100.380.305",
        name="NO_FRONTEND_INFORMATION_PROVIDED_FOR_ASYNCHRONOUS_TRANSACTION",
        description="no frontend information provided for asynchronous transaction",
    )
    NO_AUTHENTICATION_DATA_PROVIDED_IN_RISK_MANAGEMENT_TRANSACTION = ResultCode(
        code="100.380.306",
        name="NO_AUTHENTICATION_DATA_PROVIDED_IN_RISK_MANAGEMENT_TRANSACTION",
        description="no authentication data provided in risk management transaction",
    )
    USER_AUTHENTICATION_FAILED = ResultCode(
        code="100.380.401", name="USER_AUTHENTICATION_FAILED", description="User Authentication Failed"
    )
    RISK_MANAGEMENT_TRANSACTION_TIMEOUT = ResultCode(
        code="100.380.501",
        name="RISK_MANAGEMENT_TRANSACTION_TIMEOUT",
        description="risk management transaction timeout",
    )
    PURCHASE_AMOUNT_CURRENCY_MISMATCH = ResultCode(
        code="100.390.101", name="PURCHASE_AMOUNT_CURRENCY_MISMATCH", description="purchase amount/currency mismatch"
    )
    PARES_VALIDATION_FAILED = ResultCode(
        code="100.390.102", name="PARES_VALIDATION_FAILED", description="PARes Validation failed"
    )
    PARES_VALIDATION_FAILED__PROBLEM_WITH_SIGNATURE = ResultCode(
        code="100.390.103",
        name="PARES_VALIDATION_FAILED__PROBLEM_WITH_SIGNATURE",
        description="PARes Validation failed - problem with signature",
    )
    XID_MISMATCH = ResultCode(code="100.390.104", name="XID_MISMATCH", description="XID mismatch")
    TRANSACTION_REJECTED_BECAUSE_OF_TECHNICAL_ERROR_IN_3DSECURE_SYSTEM = ResultCode(
        code="100.390.105",
        name="TRANSACTION_REJECTED_BECAUSE_OF_TECHNICAL_ERROR_IN_3DSECURE_SYSTEM",
        description="Transaction rejected because of technical error in 3DSecure system",
    )
    TRANSACTION_REJECTED_BECAUSE_OF_ERROR_IN_3DSECURE_CONFIGURATION = ResultCode(
        code="100.390.106",
        name="TRANSACTION_REJECTED_BECAUSE_OF_ERROR_IN_3DSECURE_CONFIGURATION",
        description="Transaction rejected because of error in 3DSecure configuration",
    )
    TRANSACTION_REJECTED_BECAUSE_CARDHOLDER_AUTHENTICATION_UNAVAILABLE = ResultCode(
        code="100.390.107",
        name="TRANSACTION_REJECTED_BECAUSE_CARDHOLDER_AUTHENTICATION_UNAVAILABLE",
        description="Transaction rejected because cardholder authentication unavailable",
    )
    TRANSACTION_REJECTED_BECAUSE_MERCHANT_NOT_PARTICIPATING_IN_3DSECURE_PROGRAM = ResultCode(
        code="100.390.108",
        name="TRANSACTION_REJECTED_BECAUSE_MERCHANT_NOT_PARTICIPATING_IN_3DSECURE_PROGRAM",
        description="Transaction rejected because merchant not participating in 3DSecure program",
    )
    TRANSACTION_REJECTED_BECAUSE_OF_VISA_STATUS_U_OR_AMEX_STATUS_N_OR_U_IN_3DSECURE_PROGRAM = ResultCode(
        code="100.390.109",
        name="TRANSACTION_REJECTED_BECAUSE_OF_VISA_STATUS_U_OR_AMEX_STATUS_N_OR_U_IN_3DSECURE_PROGRAM",
        description="Transaction rejected because of VISA status 'U' or AMEX status 'N' or 'U' in 3DSecure program",
    )
    CARDHOLDER_NOT_FOUND__CARD_NUMBER_PROVIDED_IS_NOT_FOUND_IN_THE_RANGES_OF_THE_ISSUER_2 = ResultCode(
        code="100.390.110",
        name="CARDHOLDER_NOT_FOUND__CARD_NUMBER_PROVIDED_IS_NOT_FOUND_IN_THE_RANGES_OF_THE_ISSUER_2",
        description="Cardholder Not Found - card number provided is not found in the ranges of the issuer",
    )
    COMMUNICATION_ERROR_TO_SCHEME_DIRECTORY_SERVER_2 = ResultCode(
        code="100.390.111",
        name="COMMUNICATION_ERROR_TO_SCHEME_DIRECTORY_SERVER_2",
        description="Communication Error to Scheme Directory Server",
    )
    TECHNICAL_ERROR_IN_3D_SYSTEM_2 = ResultCode(
        code="100.390.112", name="TECHNICAL_ERROR_IN_3D_SYSTEM_2", description="Technical Error in 3D system"
    )
    UNSUPPORTED_USER_DEVICE__AUTHENTICATION_NOT_POSSIBLE_2 = ResultCode(
        code="100.390.113",
        name="UNSUPPORTED_USER_DEVICE__AUTHENTICATION_NOT_POSSIBLE_2",
        description="Unsupported User Device - Authentication not possible",
    )
    NOT_AUTHENTICATED_BECAUSE_THE_ISSUER_IS_REJECTING_AUTHENTICATION = ResultCode(
        code="100.390.114",
        name="NOT_AUTHENTICATED_BECAUSE_THE_ISSUER_IS_REJECTING_AUTHENTICATION",
        description="Not authenticated because the issuer is rejecting authentication",
    )
    AUTHENTICATION_FAILED_DUE_TO_INVALID_MESSAGE_FORMAT = ResultCode(
        code="100.390.115",
        name="AUTHENTICATION_FAILED_DUE_TO_INVALID_MESSAGE_FORMAT",
        description="Authentication failed due to invalid message format",
    )
    ACCESS_DENIED_TO_THE_AUTHENTICATION_SYSTEM = ResultCode(
        code="100.390.116",
        name="ACCESS_DENIED_TO_THE_AUTHENTICATION_SYSTEM",
        description="Access denied to the authentication system",
    )
    AUTHENTICATION_FAILED_DUE_TO_INVALID_DATA_FIELDS = ResultCode(
        code="100.390.117",
        name="AUTHENTICATION_FAILED_DUE_TO_INVALID_DATA_FIELDS",
        description="Authentication failed due to invalid data fields",
    )
    AUTHENTICATION_FAILED_DUE_TO_SUSPECTED_FRAUD = ResultCode(
        code="100.390.118",
        name="AUTHENTICATION_FAILED_DUE_TO_SUSPECTED_FRAUD",
        description="Authentication failed due to suspected fraud",
    )
    BANK_NOT_SUPPORTED_FOR_GIROPAY = ResultCode(
        code="100.395.101", name="BANK_NOT_SUPPORTED_FOR_GIROPAY", description="Bank not supported for Giropay"
    )
    ACCOUNT_NOT_ENABLED_FOR_GIROPAY_EG_TEST_ACCOUNT = ResultCode(
        code="100.395.102",
        name="ACCOUNT_NOT_ENABLED_FOR_GIROPAY_EG_TEST_ACCOUNT",
        description="Account not enabled for Giropay e.g. test account",
    )
    PREVIOUSLY_PENDING_ONLINE_TRANSFER_TRANSACTION_TIMED_OUT = ResultCode(
        code="100.395.501",
        name="PREVIOUSLY_PENDING_ONLINE_TRANSFER_TRANSACTION_TIMED_OUT",
        description="Previously pending online transfer transaction timed out",
    )
    ACQUIRER_BANK_REPORTED_TIMEOUT_ON_ONLINE_TRANSFER_TRANSACTION = ResultCode(
        code="100.395.502",
        name="ACQUIRER_BANK_REPORTED_TIMEOUT_ON_ONLINE_TRANSFER_TRANSACTION",
        description="Acquirer/Bank reported timeout on online transfer transaction",
    )
    CANCELLED_BY_USER = ResultCode(code="100.396.101", name="CANCELLED_BY_USER", description="Cancelled by user")
    NOT_CONFIRMED_BY_USER = ResultCode(
        code="100.396.102", name="NOT_CONFIRMED_BY_USER", description="Not confirmed by user"
    )
    PREVIOUSLY_PENDING_TRANSACTION_TIMED_OUT = ResultCode(
        code="100.396.103",
        name="PREVIOUSLY_PENDING_TRANSACTION_TIMED_OUT",
        description="Previously pending transaction timed out",
    )
    UNCERTAIN_STATUS__PROBABLY_CANCELLED_BY_USER = ResultCode(
        code="100.396.104",
        name="UNCERTAIN_STATUS__PROBABLY_CANCELLED_BY_USER",
        description="Uncertain status - probably cancelled by user",
    )
    USER_DID_NOT_AGREE_TO_PAYMENT_METHOD_TERMS = ResultCode(
        code="100.396.106",
        name="USER_DID_NOT_AGREE_TO_PAYMENT_METHOD_TERMS",
        description="User did not agree to payment method terms",
    )
    CANCELLED_BY_MERCHANT = ResultCode(
        code="100.396.201", name="CANCELLED_BY_MERCHANT", description="Cancelled by merchant"
    )
    CANCELLED_BY_USER_DUE_TO_EXTERNAL_UPDATE = ResultCode(
        code="100.397.101",
        name="CANCELLED_BY_USER_DUE_TO_EXTERNAL_UPDATE",
        description="Cancelled by user due to external update",
    )
    REJECTED_BY_CONNECTOR_ACQUIRER_DUE_TO_EXTERNAL_UPDATE = ResultCode(
        code="100.397.102",
        name="REJECTED_BY_CONNECTOR_ACQUIRER_DUE_TO_EXTERNAL_UPDATE",
        description="Rejected by connector/acquirer due to external update",
    )
    TRANSACTION_DECLINED_WRONG_ADDRESS_1 = ResultCode(
        code="100.400.000",
        name="TRANSACTION_DECLINED_WRONG_ADDRESS_1",
        description="transaction declined (Wrong Address)",
    )
    TRANSACTION_DECLINED_WRONG_IDENTIFICATION_1 = ResultCode(
        code="100.400.001",
        name="TRANSACTION_DECLINED_WRONG_IDENTIFICATION_1",
        description="transaction declined (Wrong Identification)",
    )
    TRANSACTION_DECLINED_INSUFFICIENT_CREDIBILITY_SCORE_1 = ResultCode(
        code="100.400.002",
        name="TRANSACTION_DECLINED_INSUFFICIENT_CREDIBILITY_SCORE_1",
        description="transaction declined (Insufficient credibility score)",
    )
    TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_3 = ResultCode(
        code="100.400.005",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_3",
        description="transaction must be executed for German address",
    )
    SYSTEM_ERROR__POSSIBLE_INCORRECT_MISSING_INPUT_DATA = ResultCode(
        code="100.400.007",
        name="SYSTEM_ERROR__POSSIBLE_INCORRECT_MISSING_INPUT_DATA",
        description="System error ( possible incorrect/missing input data)",
    )
    TRANSACTION_DECLINED_3 = ResultCode(
        code="100.400.020", name="TRANSACTION_DECLINED_3", description="transaction declined"
    )
    TRANSACTION_DECLINED_FOR_COUNTRY = ResultCode(
        code="100.400.021", name="TRANSACTION_DECLINED_FOR_COUNTRY", description="transaction declined for country"
    )
    TRANSACTION_NOT_AUTHORIZED_PLEASE_CHECK_MANUALLY_2 = ResultCode(
        code="100.400.030",
        name="TRANSACTION_NOT_AUTHORIZED_PLEASE_CHECK_MANUALLY_2",
        description="transaction not authorized. Please check manually",
    )
    TRANSACTION_DECLINED_FOR_OTHER_ERROR = ResultCode(
        code="100.400.039",
        name="TRANSACTION_DECLINED_FOR_OTHER_ERROR",
        description="transaction declined for other error",
    )
    AUTHORIZATION_FAILURE_1 = ResultCode(
        code="100.400.040", name="AUTHORIZATION_FAILURE_1", description="authorization failure"
    )
    TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_4 = ResultCode(
        code="100.400.041",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_GERMAN_ADDRESS_4",
        description="transaction must be executed for German address",
    )
    TRANSACTION_DECLINED_BY_SCHUFA_INSUFFICIENT_CREDIBILITY_SCORE = ResultCode(
        code="100.400.042",
        name="TRANSACTION_DECLINED_BY_SCHUFA_INSUFFICIENT_CREDIBILITY_SCORE",
        description="transaction declined by SCHUFA (Insufficient credibility score)",
    )
    TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_1 = ResultCode(
        code="100.400.043",
        name="TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_1",
        description="transaction declined because of missing obligatory parameter(s)",
    )
    TRANSACTION_NOT_AUTHORIZED_PLEASE_CHECK_MANUALLY_1 = ResultCode(
        code="100.400.044",
        name="TRANSACTION_NOT_AUTHORIZED_PLEASE_CHECK_MANUALLY_1",
        description="transaction not authorized. Please check manually",
    )
    SCHUFA_RESULT_NOT_DEFINITE_PLEASE_CHECK_MANUALLY = ResultCode(
        code="100.400.045",
        name="SCHUFA_RESULT_NOT_DEFINITE_PLEASE_CHECK_MANUALLY",
        description="SCHUFA result not definite. Please check manually",
    )
    SCHUFA_SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA = ResultCode(
        code="100.400.051",
        name="SCHUFA_SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA",
        description="SCHUFA system error (possible incorrect/missing input data)",
    )
    AUTHORIZATION_FAILURE_2 = ResultCode(
        code="100.400.060", name="AUTHORIZATION_FAILURE_2", description="authorization failure"
    )
    TRANSACTION_DECLINED_INSUFFICIENT_CREDIBILITY_SCORE_2 = ResultCode(
        code="100.400.061",
        name="TRANSACTION_DECLINED_INSUFFICIENT_CREDIBILITY_SCORE_2",
        description="transaction declined (Insufficient credibility score)",
    )
    TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_2 = ResultCode(
        code="100.400.063",
        name="TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_2",
        description="transaction declined because of missing obligatory parameter(s)",
    )
    TRANSACTION_MUST_BE_EXECUTED_FOR_AUSTRIAN_GERMAN_OR_SWISS_ADDRESS = ResultCode(
        code="100.400.064",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_AUSTRIAN_GERMAN_OR_SWISS_ADDRESS",
        description="transaction must be executed for Austrian, German or Swiss address",
    )
    RESULT_AMBIGUOUS_PLEASE_CHECK_MANUALLY_1 = ResultCode(
        code="100.400.065",
        name="RESULT_AMBIGUOUS_PLEASE_CHECK_MANUALLY_1",
        description="result ambiguous. Please check manually",
    )
    SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_2 = ResultCode(
        code="100.400.071",
        name="SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_2",
        description="system error (possible incorrect/missing input data)",
    )
    AUTHORIZATION_FAILURE_3 = ResultCode(
        code="100.400.080", name="AUTHORIZATION_FAILURE_3", description="authorization failure"
    )
    TRANSACTION_DECLINED_4 = ResultCode(
        code="100.400.081", name="TRANSACTION_DECLINED_4", description="transaction declined"
    )
    TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_3 = ResultCode(
        code="100.400.083",
        name="TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_3",
        description="transaction declined because of missing obligatory parameter(s)",
    )
    TRANSACTION_CAN_NOT_BE_EXECUTED_FOR_GIVEN_COUNTRY = ResultCode(
        code="100.400.084",
        name="TRANSACTION_CAN_NOT_BE_EXECUTED_FOR_GIVEN_COUNTRY",
        description="transaction can not be executed for given country",
    )
    RESULT_AMBIGUOUS_PLEASE_CHECK_MANUALLY_2 = ResultCode(
        code="100.400.085",
        name="RESULT_AMBIGUOUS_PLEASE_CHECK_MANUALLY_2",
        description="result ambiguous. Please check manually",
    )
    TRANSACTION_DECLINED_WRONG_ADDRESS_2 = ResultCode(
        code="100.400.086",
        name="TRANSACTION_DECLINED_WRONG_ADDRESS_2",
        description="transaction declined (Wrong Address)",
    )
    TRANSACTION_DECLINED_WRONG_IDENTIFICATION_2 = ResultCode(
        code="100.400.087",
        name="TRANSACTION_DECLINED_WRONG_IDENTIFICATION_2",
        description="transaction declined (Wrong Identification)",
    )
    SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_3 = ResultCode(
        code="100.400.091",
        name="SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_3",
        description="system error (possible incorrect/missing input data)",
    )
    TRANSACTION_DECLINED__VERY_BAD_RATING = ResultCode(
        code="100.400.100",
        name="TRANSACTION_DECLINED__VERY_BAD_RATING",
        description="transaction declined - very bad rating",
    )
    AUTHORIZATION_FAILURE_4 = ResultCode(
        code="100.400.120", name="AUTHORIZATION_FAILURE_4", description="authorization failure"
    )
    ACCOUNT_BLACKLISTED = ResultCode(code="100.400.121", name="ACCOUNT_BLACKLISTED", description="account blacklisted")
    TRANSACTION_MUST_BE_EXECUTED_FOR_VALID_GERMAN_ACCOUNT = ResultCode(
        code="100.400.122",
        name="TRANSACTION_MUST_BE_EXECUTED_FOR_VALID_GERMAN_ACCOUNT",
        description="transaction must be executed for valid German account",
    )
    TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_4 = ResultCode(
        code="100.400.123",
        name="TRANSACTION_DECLINED_BECAUSE_OF_MISSING_OBLIGATORY_PARAMETERS_4",
        description="transaction declined because of missing obligatory parameter(s)",
    )
    SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_4 = ResultCode(
        code="100.400.130",
        name="SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_4",
        description="system error (possible incorrect/missing input data)",
    )
    SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_5 = ResultCode(
        code="100.400.139",
        name="SYSTEM_ERROR_POSSIBLE_INCORRECT_MISSING_INPUT_DATA_5",
        description="system error (possible incorrect/missing input data)",
    )
    TRANSACTION_DECLINED_BY_GATEKEEPER = ResultCode(
        code="100.400.140", name="TRANSACTION_DECLINED_BY_GATEKEEPER", description="transaction declined by GateKeeper"
    )
    CHALLENGE_BY_RED_SHIELD = ResultCode(
        code="100.400.141", name="CHALLENGE_BY_RED_SHIELD", description="Challenge by ReD Shield"
    )
    DENY_BY_RED_SHIELD = ResultCode(code="100.400.142", name="DENY_BY_RED_SHIELD", description="Deny by ReD Shield")
    NOSCORE_BY_RED_SHIELD = ResultCode(
        code="100.400.143", name="NOSCORE_BY_RED_SHIELD", description="Noscore by ReD Shield"
    )
    RED_SHIELD_DATA_ERROR = ResultCode(
        code="100.400.144", name="RED_SHIELD_DATA_ERROR", description="ReD Shield data error"
    )
    RED_SHIELD_CONNECTION_ERROR = ResultCode(
        code="100.400.145", name="RED_SHIELD_CONNECTION_ERROR", description="ReD Shield connection error"
    )
    LINE_ITEM_ERROR_BY_RED_SHIELD = ResultCode(
        code="100.400.146", name="LINE_ITEM_ERROR_BY_RED_SHIELD", description="Line item error by ReD Shield"
    )
    PAYMENT_VOID_AND_TRANSACTION_DENIED_BY_RED_SHIELD = ResultCode(
        code="100.400.147",
        name="PAYMENT_VOID_AND_TRANSACTION_DENIED_BY_RED_SHIELD",
        description="Payment void and transaction denied by ReD Shield",
    )
    PAYMENT_VOID_AND_TRANSACTION_CHALLENGED_BY_RED_SHIELD = ResultCode(
        code="100.400.148",
        name="PAYMENT_VOID_AND_TRANSACTION_CHALLENGED_BY_RED_SHIELD",
        description="Payment void and transaction challenged by ReD Shield",
    )
    PAYMENT_VOID_AND_DATA_ERROR_BY_RED_SHIELD = ResultCode(
        code="100.400.149",
        name="PAYMENT_VOID_AND_DATA_ERROR_BY_RED_SHIELD",
        description="Payment void and data error by ReD Shield",
    )
    PAYMENT_VOID_AND_CONNECTION_ERROR_BY_RED_SHIELD = ResultCode(
        code="100.400.150",
        name="PAYMENT_VOID_AND_CONNECTION_ERROR_BY_RED_SHIELD",
        description="Payment void and connection error by ReD Shield",
    )
    PAYMENT_VOID_AND_LINE_ITEM_ERROR_BY_RED_SHIELD = ResultCode(
        code="100.400.151",
        name="PAYMENT_VOID_AND_LINE_ITEM_ERROR_BY_RED_SHIELD",
        description="Payment void and line item error by ReD Shield",
    )
    PAYMENT_VOID_AND_ERROR_RETURNED_BY_RED_SHIELD = ResultCode(
        code="100.400.152",
        name="PAYMENT_VOID_AND_ERROR_RETURNED_BY_RED_SHIELD",
        description="Payment void and error returned by ReD Shield",
    )
    CHALLENGED_BY_THREAT_METRIX = ResultCode(
        code="100.400.241", name="CHALLENGED_BY_THREAT_METRIX", description="Challenged by Threat Metrix"
    )
    DENIED_BY_THREAT_METRIX = ResultCode(
        code="100.400.242", name="DENIED_BY_THREAT_METRIX", description="Denied by Threat Metrix"
    )
    INVALID_SESSIONID = ResultCode(code="100.400.243", name="INVALID_SESSIONID", description="Invalid sessionId")
    AUTHORIZATION_FAILURE_5 = ResultCode(
        code="100.400.260", name="AUTHORIZATION_FAILURE_5", description="authorization failure"
    )
    ABORT_CHECKOUT_PROCESS = ResultCode(
        code="100.400.300", name="ABORT_CHECKOUT_PROCESS", description="abort checkout process"
    )
    REENTER_AGE_BIRTHDATE = ResultCode(
        code="100.400.301", name="REENTER_AGE_BIRTHDATE", description="reenter age/birthdate"
    )
    REENTER_ADDRESS_PACKSTATION_NOT_ALLOWED = ResultCode(
        code="100.400.302",
        name="REENTER_ADDRESS_PACKSTATION_NOT_ALLOWED",
        description="reenter address (packstation not allowed)",
    )
    REENTER_ADDRESS = ResultCode(code="100.400.303", name="REENTER_ADDRESS", description="reenter address")
    INVALID_INPUT_DATA = ResultCode(code="100.400.304", name="INVALID_INPUT_DATA", description="invalid input data")
    INVALID_FOREIGN_ADDRESS = ResultCode(
        code="100.400.305", name="INVALID_FOREIGN_ADDRESS", description="invalid foreign address"
    )
    DELIVERY_ADDRESS_ERROR = ResultCode(
        code="100.400.306", name="DELIVERY_ADDRESS_ERROR", description="delivery address error"
    )
    OFFER_ONLY_SECURE_METHODS_OF_PAYMENT = ResultCode(
        code="100.400.307",
        name="OFFER_ONLY_SECURE_METHODS_OF_PAYMENT",
        description="offer only secure methods of payment",
    )
    OFFER_ONLY_SECURE_METHODS_OF_PAYMENT_POSSIBLY_ABORT_CHECKOUT = ResultCode(
        code="100.400.308",
        name="OFFER_ONLY_SECURE_METHODS_OF_PAYMENT_POSSIBLY_ABORT_CHECKOUT",
        description="offer only secure methods of payment; possibly abort checkout",
    )
    CONFIRM_CORRECTED_ADDRESS_IF_NOT_CONFIRMED_OFFER_SECURE_METHODS_OF_PAYMENT_ONLY = ResultCode(
        code="100.400.309",
        name="CONFIRM_CORRECTED_ADDRESS_IF_NOT_CONFIRMED_OFFER_SECURE_METHODS_OF_PAYMENT_ONLY",
        description="confirm corrected address; if not confirmed, offer secure methods of payment only",
    )
    CONFIRM_BANK_ACCOUNT_DATA_IF_NOT_CONFIRMED_OFFER_SECURE_METHODS_OF_PAYMENT_ONLY = ResultCode(
        code="100.400.310",
        name="CONFIRM_BANK_ACCOUNT_DATA_IF_NOT_CONFIRMED_OFFER_SECURE_METHODS_OF_PAYMENT_ONLY",
        description="confirm bank account data; if not confirmed, offer secure methods of payment only",
    )
    TRANSACTION_DECLINED_FORMAT_ERROR_1 = ResultCode(
        code="100.400.311",
        name="TRANSACTION_DECLINED_FORMAT_ERROR_1",
        description="transaction declined (format error)",
    )
    TRANSACTION_DECLINED_INVALID_CONFIGURATION_DATA_1 = ResultCode(
        code="100.400.312",
        name="TRANSACTION_DECLINED_INVALID_CONFIGURATION_DATA_1",
        description="transaction declined (invalid configuration data)",
    )
    CURRENCY_FIELD_IS_INVALID_OR_MISSING = ResultCode(
        code="100.400.313",
        name="CURRENCY_FIELD_IS_INVALID_OR_MISSING",
        description="currency field is invalid or missing",
    )
    AMOUNT_INVALID_OR_EMPTY = ResultCode(
        code="100.400.314", name="AMOUNT_INVALID_OR_EMPTY", description="amount invalid or empty"
    )
    INVALID_OR_MISSING_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX = ResultCode(
        code="100.400.315",
        name="INVALID_OR_MISSING_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX",
        description="invalid or missing email address (probably invalid syntax)",
    )
    TRANSACTION_DECLINED_CARD_MISSING = ResultCode(
        code="100.400.316", name="TRANSACTION_DECLINED_CARD_MISSING", description="transaction declined (card missing)"
    )
    TRANSACTION_DECLINED_INVALID_CARD_1 = ResultCode(
        code="100.400.317",
        name="TRANSACTION_DECLINED_INVALID_CARD_1",
        description="transaction declined (invalid card)",
    )
    INVALID_IP_NUMBER_1 = ResultCode(code="100.400.318", name="INVALID_IP_NUMBER_1", description="invalid IP number")
    TRANSACTION_DECLINED_BY_RISK_SYSTEM = ResultCode(
        code="100.400.319",
        name="TRANSACTION_DECLINED_BY_RISK_SYSTEM",
        description="transaction declined by risk system",
    )
    SHOPPING_CART_DATA_INVALID_OR_MISSING = ResultCode(
        code="100.400.320",
        name="SHOPPING_CART_DATA_INVALID_OR_MISSING",
        description="shopping cart data invalid or missing",
    )
    PAYMENT_TYPE_INVALID_OR_MISSING = ResultCode(
        code="100.400.321", name="PAYMENT_TYPE_INVALID_OR_MISSING", description="payment type invalid or missing"
    )
    ENCRYPTION_METHOD_INVALID_OR_MISSING = ResultCode(
        code="100.400.322",
        name="ENCRYPTION_METHOD_INVALID_OR_MISSING",
        description="encryption method invalid or missing",
    )
    CERTIFICATE_INVALID_OR_MISSING = ResultCode(
        code="100.400.323", name="CERTIFICATE_INVALID_OR_MISSING", description="certificate invalid or missing"
    )
    ERROR_ON_THE_EXTERNAL_RISK_SYSTEM = ResultCode(
        code="100.400.324", name="ERROR_ON_THE_EXTERNAL_RISK_SYSTEM", description="Error on the external risk system"
    )
    EXTERNAL_RISK_SYSTEM_NOT_AVAILABLE = ResultCode(
        code="100.400.325", name="EXTERNAL_RISK_SYSTEM_NOT_AVAILABLE", description="External risk system not available"
    )
    RISK_BANK_ACCOUNT_CHECK_UNSUCCESSFUL = ResultCode(
        code="100.400.326",
        name="RISK_BANK_ACCOUNT_CHECK_UNSUCCESSFUL",
        description="Risk bank account check unsuccessful",
    )
    RISK_REPORT_UNSUCCESSFUL = ResultCode(
        code="100.400.327", name="RISK_REPORT_UNSUCCESSFUL", description="Risk report unsuccessful"
    )
    RISK_REPORT_UNSUCCESSFUL_INVALID_DATA = ResultCode(
        code="100.400.328",
        name="RISK_REPORT_UNSUCCESSFUL_INVALID_DATA",
        description="Risk report unsuccessful (invalid data)",
    )
    WAITING_FOR_EXTERNAL_RISK = ResultCode(
        code="100.400.500", name="WAITING_FOR_EXTERNAL_RISK", description="waiting for external risk"
    )
    PAYMENT_METHOD_INVALID = ResultCode(
        code="100.500.101", name="PAYMENT_METHOD_INVALID", description="payment method invalid"
    )
    PAYMENT_TYPE_INVALID = ResultCode(
        code="100.500.201", name="PAYMENT_TYPE_INVALID", description="payment type invalid"
    )
    INVALID_DUE_DATE = ResultCode(code="100.500.301", name="INVALID_DUE_DATE", description="invalid due date")
    INVALID_MANDATE_DATE_OF_SIGNATURE = ResultCode(
        code="100.500.302", name="INVALID_MANDATE_DATE_OF_SIGNATURE", description="invalid mandate date of signature"
    )
    INVALID_MANDATE_ID = ResultCode(code="100.500.303", name="INVALID_MANDATE_ID", description="invalid mandate id")
    INVALID_MANDATE_EXTERNAL_ID = ResultCode(
        code="100.500.304", name="INVALID_MANDATE_EXTERNAL_ID", description="invalid mandate external id"
    )
    REQUEST_CONTAINS_NO_AMOUNT_OR_TOO_LOW_AMOUNT = ResultCode(
        code="100.550.300",
        name="REQUEST_CONTAINS_NO_AMOUNT_OR_TOO_LOW_AMOUNT",
        description="request contains no amount or too low amount",
    )
    AMOUNT_TOO_LARGE = ResultCode(code="100.550.301", name="AMOUNT_TOO_LARGE", description="amount too large")
    AMOUNT_FORMAT_INVALID_ONLY_TWO_DECIMALS_ALLOWED = ResultCode(
        code="100.550.303",
        name="AMOUNT_FORMAT_INVALID_ONLY_TWO_DECIMALS_ALLOWED",
        description="amount format invalid (only two decimals allowed).",
    )
    AMOUNT_EXCEEDS_LIMIT_FOR_THE_REGISTERED_ACCOUNT = ResultCode(
        code="100.550.310",
        name="AMOUNT_EXCEEDS_LIMIT_FOR_THE_REGISTERED_ACCOUNT",
        description="amount exceeds limit for the registered account.",
    )
    EXCEEDING_ACCOUNT_BALANCE = ResultCode(
        code="100.550.311", name="EXCEEDING_ACCOUNT_BALANCE", description="exceeding account balance"
    )
    AMOUNT_IS_OUTSIDE_ALLOWED_TICKET_SIZE_BOUNDARIES = ResultCode(
        code="100.550.312",
        name="AMOUNT_IS_OUTSIDE_ALLOWED_TICKET_SIZE_BOUNDARIES",
        description="Amount is outside allowed ticket size boundaries",
    )
    REQUEST_CONTAINS_NO_CURRENCY = ResultCode(
        code="100.550.400", name="REQUEST_CONTAINS_NO_CURRENCY", description="request contains no currency"
    )
    INVALID_CURRENCY = ResultCode(code="100.550.401", name="INVALID_CURRENCY", description="invalid currency")
    RISK_AMOUNT_TOO_LARGE = ResultCode(
        code="100.550.601", name="RISK_AMOUNT_TOO_LARGE", description="risk amount too large"
    )
    RISK_AMOUNT_FORMAT_INVALID_ONLY_TWO_DECIMALS_ALLOWED = ResultCode(
        code="100.550.603",
        name="RISK_AMOUNT_FORMAT_INVALID_ONLY_TWO_DECIMALS_ALLOWED",
        description="risk amount format invalid (only two decimals allowed)",
    )
    RISK_AMOUNT_IS_SMALLER_THAN_AMOUNT_IT_MUST_BE_EQUAL_OR_BIGGER_THEN_AMOUNT = ResultCode(
        code="100.550.605",
        name="RISK_AMOUNT_IS_SMALLER_THAN_AMOUNT_IT_MUST_BE_EQUAL_OR_BIGGER_THEN_AMOUNT",
        description="risk amount is smaller than amount (it must be equal or bigger then amount)",
    )
    AMOUNTS_NOT_MATCHED = ResultCode(code="100.550.701", name="AMOUNTS_NOT_MATCHED", description="amounts not matched")
    CURRENCIES_NOT_MATCHED = ResultCode(
        code="100.550.702", name="CURRENCIES_NOT_MATCHED", description="currencies not matched"
    )
    USAGE_FIELD_TOO_LONG = ResultCode(
        code="100.600.500", name="USAGE_FIELD_TOO_LONG", description="usage field too long"
    )
    CUSTOMER_SURNAME_MAY_NOT_BE_NULL = ResultCode(
        code="100.700.100", name="CUSTOMER_SURNAME_MAY_NOT_BE_NULL", description="customer.surname may not be null"
    )
    CUSTOMER_SURNAME_LENGTH_MUST_BE_BETWEEN_0_AND_50 = ResultCode(
        code="100.700.101",
        name="CUSTOMER_SURNAME_LENGTH_MUST_BE_BETWEEN_0_AND_50",
        description="customer.surname length must be between 0 and 50",
    )
    CUSTOMER_GIVENNAME_MAY_NOT_BE_NULL = ResultCode(
        code="100.700.200", name="CUSTOMER_GIVENNAME_MAY_NOT_BE_NULL", description="customer.givenName may not be null"
    )
    CUSTOMER_GIVENNAME_LENGTH_MUST_BE_BETWEEN_0_AND_50 = ResultCode(
        code="100.700.201",
        name="CUSTOMER_GIVENNAME_LENGTH_MUST_BE_BETWEEN_0_AND_50",
        description="customer.givenName length must be between 0 and 50",
    )
    INVALID_SALUTATION = ResultCode(code="100.700.300", name="INVALID_SALUTATION", description="invalid salutation")
    INVALID_TITLE = ResultCode(code="100.700.400", name="INVALID_TITLE", description="invalid title")
    COMPANY_NAME_TOO_LONG_1 = ResultCode(
        code="100.700.500", name="COMPANY_NAME_TOO_LONG_1", description="company name too long"
    )
    IDENTITY_CONTAINS_NO_OR_INVALID_PAPER = ResultCode(
        code="100.700.800",
        name="IDENTITY_CONTAINS_NO_OR_INVALID_PAPER",
        description="identity contains no or invalid 'paper'",
    )
    IDENTITY_CONTAINS_NO_OR_INVALID_IDENTIFICATION_VALUE = ResultCode(
        code="100.700.801",
        name="IDENTITY_CONTAINS_NO_OR_INVALID_IDENTIFICATION_VALUE",
        description="identity contains no or invalid identification value",
    )
    IDENTIFICATION_VALUE_TOO_LONG = ResultCode(
        code="100.700.802", name="IDENTIFICATION_VALUE_TOO_LONG", description="identification value too long"
    )
    SPECIFY_AT_LEAST_ONE_IDENTITY = ResultCode(
        code="100.700.810", name="SPECIFY_AT_LEAST_ONE_IDENTITY", description="specify at least one identity"
    )
    REQUEST_CONTAINS_NO_STREET = ResultCode(
        code="100.800.100", name="REQUEST_CONTAINS_NO_STREET", description="request contains no street"
    )
    THE_COMBINATION_OF_STREET1_AND_STREET2_MUST_NOT_EXCEED_201_CHARACTERS = ResultCode(
        code="100.800.101",
        name="THE_COMBINATION_OF_STREET1_AND_STREET2_MUST_NOT_EXCEED_201_CHARACTERS",
        description="The combination of street1 and street2 must not exceed 201 characters.",
    )
    THE_COMBINATION_OF_STREET1_AND_STREET2_MUST_NOT_CONTAIN_ONLY_NUMBERS = ResultCode(
        code="100.800.102",
        name="THE_COMBINATION_OF_STREET1_AND_STREET2_MUST_NOT_CONTAIN_ONLY_NUMBERS",
        description="The combination of street1 and street2 must not contain only numbers.",
    )
    REQUEST_CONTAINS_NO_ZIP = ResultCode(
        code="100.800.200", name="REQUEST_CONTAINS_NO_ZIP", description="request contains no zip"
    )
    ZIP_TOO_LONG = ResultCode(code="100.800.201", name="ZIP_TOO_LONG", description="zip too long")
    INVALID_ZIP_1 = ResultCode(code="100.800.202", name="INVALID_ZIP_1", description="invalid zip")
    REQUEST_CONTAINS_NO_CITY = ResultCode(
        code="100.800.300", name="REQUEST_CONTAINS_NO_CITY", description="request contains no city"
    )
    CITY_TOO_LONG = ResultCode(code="100.800.301", name="CITY_TOO_LONG", description="city too long")
    INVALID_CITY_1 = ResultCode(code="100.800.302", name="INVALID_CITY_1", description="invalid city")
    INVALID_STATE_COUNTRY_COMBINATION = ResultCode(
        code="100.800.400", name="INVALID_STATE_COUNTRY_COMBINATION", description="invalid state/country combination"
    )
    STATE_TOO_LONG = ResultCode(code="100.800.401", name="STATE_TOO_LONG", description="state too long")
    REQUEST_CONTAINS_NO_COUNTRY = ResultCode(
        code="100.800.500", name="REQUEST_CONTAINS_NO_COUNTRY", description="request contains no country"
    )
    INVALID_COUNTRY = ResultCode(code="100.800.501", name="INVALID_COUNTRY", description="invalid country")
    REQUEST_CONTAINS_NO_EMAIL_ADDRESS = ResultCode(
        code="100.900.100", name="REQUEST_CONTAINS_NO_EMAIL_ADDRESS", description="request contains no email address"
    )
    INVALID_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX_1 = ResultCode(
        code="100.900.101",
        name="INVALID_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX_1",
        description="invalid email address (probably invalid syntax)",
    )
    EMAIL_ADDRESS_TOO_LONG_MAX_50_CHARS = ResultCode(
        code="100.900.105",
        name="EMAIL_ADDRESS_TOO_LONG_MAX_50_CHARS",
        description="email address too long (max 50 chars)",
    )
    INVALID_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG_1 = ResultCode(
        code="100.900.200",
        name="INVALID_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG_1",
        description="invalid phone number (has to start with a digit or a '+', at least 7 and max 25 chars long)",
    )
    INVALID_MOBILE_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG = ResultCode(
        code="100.900.300",
        name="INVALID_MOBILE_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG",
        description="invalid mobile phone number (has to start with a digit or a '+', "
        "at least 7 and max 25 chars long)",
    )
    MOBILE_PHONE_NUMBER_MANDATORY = ResultCode(
        code="100.900.301", name="MOBILE_PHONE_NUMBER_MANDATORY", description="mobile phone number mandatory"
    )
    REQUEST_CONTAINS_NO_IP_NUMBER = ResultCode(
        code="100.900.400", name="REQUEST_CONTAINS_NO_IP_NUMBER", description="request contains no ip number"
    )
    INVALID_IP_NUMBER_2 = ResultCode(code="100.900.401", name="INVALID_IP_NUMBER_2", description="invalid ip number")
    INVALID_BIRTHDATE_1 = ResultCode(code="100.900.450", name="INVALID_BIRTHDATE_1", description="invalid birthdate")
    INVALID_RECURRENCE_MODE = ResultCode(
        code="100.900.500", name="INVALID_RECURRENCE_MODE", description="invalid recurrence mode"
    )
    INVALID_REQUEST_MESSAGE_NO_VALID_XML_XML_MUST_BE_URLENCODED_MAYBE_IT_CONTAINS_A_NOT_ENCODED_AMPERSAND_OR_SOMETHING_SIMILAR = ResultCode(  # noqa: E501
        code="200.100.101",
        name="INVALID_REQUEST_MESSAGE_NO_VALID_XML_XML_MUST_BE_URLENCODED_"
        "MAYBE_IT_CONTAINS_A_NOT_ENCODED_AMPERSAND_OR_SOMETHING_SIMILAR",
        description="invalid Request Message. No valid XML. XML must be url-encoded! "
        "maybe it contains a not encoded ampersand or something similar.",
    )
    INVALID_REQUEST_XML_LOAD_MISSING_XML_STRING_MUST_BE_SENT_WITHIN_PARAMETER_LOAD = ResultCode(
        code="200.100.102",
        name="INVALID_REQUEST_XML_LOAD_MISSING_XML_STRING_MUST_BE_SENT_WITHIN_PARAMETER_LOAD",
        description="invalid Request. XML load missing (XML string must be sent within parameter 'load')",
    )
    INVALID_REQUEST_MESSAGE_THE_REQUEST_CONTAINS_STRUCTURAL_ERRORS = ResultCode(
        code="200.100.103",
        name="INVALID_REQUEST_MESSAGE_THE_REQUEST_CONTAINS_STRUCTURAL_ERRORS",
        description="invalid Request Message. The request contains structural errors",
    )
    TRANSACTION_OF_MULTIREQUEST_NOT_PROCESSED_BECAUSE_OF_SUBSEQUENT_PROBLEMS = ResultCode(
        code="200.100.150",
        name="TRANSACTION_OF_MULTIREQUEST_NOT_PROCESSED_BECAUSE_OF_SUBSEQUENT_PROBLEMS",
        description="transaction of multirequest not processed because of subsequent problems",
    )
    MULTIREQUEST_IS_ALLOWED_WITH_A_MAXIMUM_OF_10_TRANSACTIONS_ONLY = ResultCode(
        code="200.100.151",
        name="MULTIREQUEST_IS_ALLOWED_WITH_A_MAXIMUM_OF_10_TRANSACTIONS_ONLY",
        description="multi-request is allowed with a maximum of 10 transactions only",
    )
    WRONG_WEB_INTERFACE__URL_USED_PLEASE_CHECK_OUT_THE_TECH_QUICK_START_DOC_CHAPTER_3 = ResultCode(
        code="200.100.199",
        name="WRONG_WEB_INTERFACE__URL_USED_PLEASE_CHECK_OUT_THE_TECH_QUICK_START_DOC_CHAPTER_3",
        description="Wrong Web Interface / URL used. Please check out the Tech Quick Start Doc Chapter 3.",
    )
    INVALID_REQUEST_TRANSACTION_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.201",
        name="INVALID_REQUEST_TRANSACTION_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_PAYMENT_TAG_NO_OR_INVALID_CODE_SPECIFIED = ResultCode(
        code="200.100.300",
        name="INVALID_REQUEST_TRANSACTION_PAYMENT_TAG_NO_OR_INVALID_CODE_SPECIFIED",
        description="invalid Request/Transaction/Payment tag (no or invalid code specified)",
    )
    INVALID_REQUEST_TRANSACTION_PAYMENT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.301",
        name="INVALID_REQUEST_TRANSACTION_PAYMENT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Payment tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_PAYMENT_PRESENTATION_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.302",
        name="INVALID_REQUEST_TRANSACTION_PAYMENT_PRESENTATION_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Payment/Presentation tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_ACCOUNT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.401",
        name="INVALID_REQUEST_TRANSACTION_ACCOUNT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Account tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_ACCOUNT_CUSTOMER_RELEVANCE_TAG_ONE_OF_ACCOUNT_CUSTOMER_RELEVANCE_MUST_BE_PRESENT = (
        ResultCode(  # noqa: E501
            code="200.100.402",
            name="INVALID_REQUEST_TRANSACTION_ACCOUNT_CUSTOMER_RELEVANCE_TAG_"
            "ONE_OF_ACCOUNT_CUSTOMER_RELEVANCE_MUST_BE_PRESENT",
            description="invalid Request/Transaction/Account(Customer, Relevance) tag "
            "(one of Account/Customer/Relevance must be present)",
        )
    )
    INVALID_REQUEST_TRANSACTION_ANALYSIS_TAG_CRITERIONS_MUST_HAVE_A_NAME_AND_VALUE = ResultCode(
        code="200.100.403",
        name="INVALID_REQUEST_TRANSACTION_ANALYSIS_TAG_CRITERIONS_MUST_HAVE_A_NAME_AND_VALUE",
        description="invalid Request/Transaction/Analysis tag (Criterions must have a name and value)",
    )
    INVALID_REQUEST_TRANSACTION_ACCOUNT_MUST_NOT_BE_PRESENT = ResultCode(
        code="200.100.404",
        name="INVALID_REQUEST_TRANSACTION_ACCOUNT_MUST_NOT_BE_PRESENT",
        description="invalid Request/Transaction/Account (must not be present)",
    )
    INVALID_OR_MISSING_CUSTOMER = ResultCode(
        code="200.100.501", name="INVALID_OR_MISSING_CUSTOMER", description="invalid or missing customer"
    )
    INVALID_REQUEST_TRANSACTION_CUSTOMER_NAME_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.502",
        name="INVALID_REQUEST_TRANSACTION_CUSTOMER_NAME_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Customer/Name tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_CUSTOMER_CONTACT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.503",
        name="INVALID_REQUEST_TRANSACTION_CUSTOMER_CONTACT_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Customer/Contact tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_CUSTOMER_ADDRESS_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.504",
        name="INVALID_REQUEST_TRANSACTION_CUSTOMER_ADDRESS_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/Customer/Address tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.601",
        name="INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/(ApplePay|GooglePay) tag (not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_PAYMENTTOKEN_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY = ResultCode(
        code="200.100.602",
        name="INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_PAYMENTTOKEN_TAG_NOT_PRESENT_OR_PARTIALLY_EMPTY",
        description="invalid Request/Transaction/(ApplePay|GooglePay)/PaymentToken tag "
        "(not present or [partially] empty)",
    )
    INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_PAYMENTTOKEN_TAG_DECRYPTION_ERROR = ResultCode(
        code="200.100.603",
        name="INVALID_REQUEST_TRANSACTION_APPLEPAY_GOOGLEPAY_PAYMENTTOKEN_TAG_DECRYPTION_ERROR",
        description="invalid Request/Transaction/(ApplePay|GooglePay)/PaymentToken tag (decryption error)",
    )
    DUPLICATE_TRANSACTION_PLEASE_VERIFY_THAT_THE_UUID_IS_UNIQUE = ResultCode(
        code="200.200.106",
        name="DUPLICATE_TRANSACTION_PLEASE_VERIFY_THAT_THE_UUID_IS_UNIQUE",
        description="duplicate transaction. Please verify that the UUID is unique",
    )
    INVALID_HTTP_METHOD = ResultCode(code="200.300.403", name="INVALID_HTTP_METHOD", description="Invalid HTTP method")
    INVALID_OR_MISSING_PARAMETER = ResultCode(
        code="200.300.404", name="INVALID_OR_MISSING_PARAMETER", description="invalid or missing parameter"
    )
    DUPLICATE_ENTITY = ResultCode(code="200.300.405", name="DUPLICATE_ENTITY", description="Duplicate entity")
    ENTITY_NOT_FOUND = ResultCode(code="200.300.406", name="ENTITY_NOT_FOUND", description="Entity not found")
    ENTITY_NOT_SPECIFIC_ENOUGH = ResultCode(
        code="200.300.407", name="ENTITY_NOT_SPECIFIC_ENOUGH", description="Entity not specific enough"
    )
    TRANSACTION_DECLINED_ADDITIONAL_CUSTOMER_AUTHENTICATION_REQUIRED = ResultCode(
        code="300.100.100",
        name="TRANSACTION_DECLINED_ADDITIONAL_CUSTOMER_AUTHENTICATION_REQUIRED",
        description="Transaction declined (additional customer authentication required)",
    )
    CHANNEL_MERCHANT_IS_DISABLED_NO_PROCESSING_POSSIBLE = ResultCode(
        code="500.100.201",
        name="CHANNEL_MERCHANT_IS_DISABLED_NO_PROCESSING_POSSIBLE",
        description="Channel/Merchant is disabled (no processing possible)",
    )
    CHANNEL_MERCHANT_IS_NEW_NO_PROCESSING_POSSIBLE_YET = ResultCode(
        code="500.100.202",
        name="CHANNEL_MERCHANT_IS_NEW_NO_PROCESSING_POSSIBLE_YET",
        description="Channel/Merchant is new (no processing possible yet)",
    )
    CHANNEL_MERCHANT_IS_CLOSED_NO_PROCESSING_POSSIBLE = ResultCode(
        code="500.100.203",
        name="CHANNEL_MERCHANT_IS_CLOSED_NO_PROCESSING_POSSIBLE",
        description="Channel/Merchant is closed (no processing possible)",
    )
    MERCHANT_CONNECTOR_IS_DISABLED_NO_PROCESSING_POSSIBLE = ResultCode(
        code="500.100.301",
        name="MERCHANT_CONNECTOR_IS_DISABLED_NO_PROCESSING_POSSIBLE",
        description="Merchant-Connector is disabled (no processing possible)",
    )
    MERCHANT_CONNECTOR_IS_NEW_NO_PROCESSING_POSSIBLE_YET = ResultCode(
        code="500.100.302",
        name="MERCHANT_CONNECTOR_IS_NEW_NO_PROCESSING_POSSIBLE_YET",
        description="Merchant-Connector is new (no processing possible yet)",
    )
    MERCHANT_CONNECTOR_IS_CLOSED_NO_PROCESSING_POSSIBLE = ResultCode(
        code="500.100.303",
        name="MERCHANT_CONNECTOR_IS_CLOSED_NO_PROCESSING_POSSIBLE",
        description="Merchant-Connector is closed (no processing possible)",
    )
    MERCHANT_CONNECTOR_IS_DISABLED_AT_GATEWAY_NO_PROCESSING_POSSIBLE = ResultCode(
        code="500.100.304",
        name="MERCHANT_CONNECTOR_IS_DISABLED_AT_GATEWAY_NO_PROCESSING_POSSIBLE",
        description="Merchant-Connector is disabled at gateway (no processing possible)",
    )
    CONNECTOR_IS_UNAVAILABLE_NO_PROCESSING_POSSIBLE_1 = ResultCode(
        code="500.100.401",
        name="CONNECTOR_IS_UNAVAILABLE_NO_PROCESSING_POSSIBLE_1",
        description="Connector is unavailable (no processing possible)",
    )
    CONNECTOR_IS_NEW_NO_PROCESSING_POSSIBLE_YET = ResultCode(
        code="500.100.402",
        name="CONNECTOR_IS_NEW_NO_PROCESSING_POSSIBLE_YET",
        description="Connector is new (no processing possible yet)",
    )
    CONNECTOR_IS_UNAVAILABLE_NO_PROCESSING_POSSIBLE_2 = ResultCode(
        code="500.100.403",
        name="CONNECTOR_IS_UNAVAILABLE_NO_PROCESSING_POSSIBLE_2",
        description="Connector is unavailable (no processing possible)",
    )
    NO_TARGET_ACCOUNT_CONFIGURED_FOR_DD_TRANSACTION = ResultCode(
        code="500.200.101",
        name="NO_TARGET_ACCOUNT_CONFIGURED_FOR_DD_TRANSACTION",
        description="No target account configured for DD transaction",
    )
    UNEXPECTED_INTEGRATOR_ERROR_REQUEST_COULD_NOT_BE_PROCESSED = ResultCode(
        code="600.100.100",
        name="UNEXPECTED_INTEGRATOR_ERROR_REQUEST_COULD_NOT_BE_PROCESSED",
        description="Unexpected Integrator Error (Request could not be processed)",
    )
    INVALID_PAYMENT_METHOD = ResultCode(
        code="600.200.100", name="INVALID_PAYMENT_METHOD", description="invalid Payment Method"
    )
    UNSUPPORTED_PAYMENT_METHOD = ResultCode(
        code="600.200.200", name="UNSUPPORTED_PAYMENT_METHOD", description="Unsupported Payment Method"
    )
    CHANNEL_MERCHANT_NOT_CONFIGURED_FOR_THIS_PAYMENT_METHOD = ResultCode(
        code="600.200.201",
        name="CHANNEL_MERCHANT_NOT_CONFIGURED_FOR_THIS_PAYMENT_METHOD",
        description="Channel/Merchant not configured for this payment method",
    )
    CHANNEL_MERCHANT_NOT_CONFIGURED_FOR_THIS_PAYMENT_TYPE = ResultCode(
        code="600.200.202",
        name="CHANNEL_MERCHANT_NOT_CONFIGURED_FOR_THIS_PAYMENT_TYPE",
        description="Channel/Merchant not configured for this payment type",
    )
    INVALID_PAYMENT_TYPE = ResultCode(
        code="600.200.300", name="INVALID_PAYMENT_TYPE", description="invalid Payment Type"
    )
    INVALID_PAYMENT_TYPE_FOR_GIVEN_PAYMENT_METHOD = ResultCode(
        code="600.200.310",
        name="INVALID_PAYMENT_TYPE_FOR_GIVEN_PAYMENT_METHOD",
        description="invalid Payment Type for given Payment Method",
    )
    UNSUPPORTED_PAYMENT_TYPE = ResultCode(
        code="600.200.400", name="UNSUPPORTED_PAYMENT_TYPE", description="Unsupported Payment Type"
    )
    INVALID_PAYMENT_DATA_YOU_ARE_NOT_CONFIGURED_FOR_THIS_CURRENCY_OR_SUB_TYPE_COUNTRY_OR_BRAND = ResultCode(
        code="600.200.500",
        name="INVALID_PAYMENT_DATA_YOU_ARE_NOT_CONFIGURED_FOR_THIS_CURRENCY_OR_SUB_TYPE_COUNTRY_OR_BRAND",
        description="Invalid payment data. You are not configured for this currency or sub type (country or brand)",
    )
    INVALID_PAYMENT_DATA_FOR_RECURRING_TRANSACTION_MERCHANT_OR_TRANSACTION_DATA_HAS_WRONG_RECURRING_CONFIGURATION = (
        ResultCode(  # noqa: E501
            code="600.200.501",
            name="INVALID_PAYMENT_DATA_FOR_RECURRING_TRANSACTION_"
            "MERCHANT_OR_TRANSACTION_DATA_HAS_WRONG_RECURRING_CONFIGURATION",
            description="Invalid payment data for Recurring transaction. "
            "Merchant or transaction data has wrong recurring configuration.",
        )
    )
    INVALID_PAYMENT_CODE_TYPE_OR_METHOD = ResultCode(
        code="600.200.600",
        name="INVALID_PAYMENT_CODE_TYPE_OR_METHOD",
        description="invalid payment code (type or method)",
    )
    INVALID_PAYMENT_MODE_YOU_ARE_NOT_CONFIGURED_FOR_THE_REQUESTED_TRANSACTION_MODE = ResultCode(
        code="600.200.700",
        name="INVALID_PAYMENT_MODE_YOU_ARE_NOT_CONFIGURED_FOR_THE_REQUESTED_TRANSACTION_MODE",
        description="invalid payment mode (you are not configured for the requested transaction mode)",
    )
    TESTMODE_NOT_ALLOWED = ResultCode(
        code="600.200.701", name="TESTMODE_NOT_ALLOWED", description="testMode not allowed"
    )
    INVALID_BRAND_FOR_GIVEN_PAYMENT_METHOD_AND_PAYMENT_MODE_YOU_ARE_NOT_CONFIGURED_FOR_THE_REQUESTED_TRANSACTION_MODE = ResultCode(  # noqa: E501
        code="600.200.800",
        name="INVALID_BRAND_FOR_GIVEN_PAYMENT_METHOD_AND_PAYMENT_MODE_"
        "YOU_ARE_NOT_CONFIGURED_FOR_THE_REQUESTED_TRANSACTION_MODE",
        description="invalid brand for given payment method and payment mode "
        "(you are not configured for the requested transaction mode)",
    )
    INVALID_RETURN_CODE_PROVIDED = ResultCode(
        code="600.200.810", name="INVALID_RETURN_CODE_PROVIDED", description="invalid return code provided"
    )
    MERCHANT_KEY_NOT_FOUND = ResultCode(
        code="600.300.101", name="MERCHANT_KEY_NOT_FOUND", description="Merchant key not found"
    )
    MERCHANT_SOURCE_IP_ADDRESS_NOT_WHITELISTED = ResultCode(
        code="600.300.200",
        name="MERCHANT_SOURCE_IP_ADDRESS_NOT_WHITELISTED",
        description="merchant source IP address not whitelisted",
    )
    MERCHANT_NOTIFICATIONURL_NOT_WHITELISTED = ResultCode(
        code="600.300.210",
        name="MERCHANT_NOTIFICATIONURL_NOT_WHITELISTED",
        description="merchant notificationUrl not whitelisted",
    )
    SHOPPERRESULTURL_NOT_WHITELISTED = ResultCode(
        code="600.300.211", name="SHOPPERRESULTURL_NOT_WHITELISTED", description="shopperResultUrl not whitelisted"
    )
    REFERENCE_ID_NOT_EXISTING = ResultCode(
        code="700.100.100", name="REFERENCE_ID_NOT_EXISTING", description="reference id not existing"
    )
    NON_MATCHING_REFERENCE_AMOUNT = ResultCode(
        code="700.100.200", name="NON_MATCHING_REFERENCE_AMOUNT", description="non matching reference amount"
    )
    INVALID_AMOUNT_PROBABLY_TOO_LARGE = ResultCode(
        code="700.100.300", name="INVALID_AMOUNT_PROBABLY_TOO_LARGE", description="invalid amount (probably too large)"
    )
    REFERENCED_PAYMENT_METHOD_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_METHOD = ResultCode(
        code="700.100.400",
        name="REFERENCED_PAYMENT_METHOD_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_METHOD",
        description="referenced payment method does not match with requested payment method",
    )
    REFERENCED_PAYMENT_CURRENCY_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_CURRENCY = ResultCode(
        code="700.100.500",
        name="REFERENCED_PAYMENT_CURRENCY_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_CURRENCY",
        description="referenced payment currency does not match with requested payment currency",
    )
    REFERENCED_MODE_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_MODE = ResultCode(
        code="700.100.600",
        name="REFERENCED_MODE_DOES_NOT_MATCH_WITH_REQUESTED_PAYMENT_MODE",
        description="referenced mode does not match with requested payment mode",
    )
    REFERENCED_TRANSACTION_IS_OF_INAPPROPRIATE_TYPE = ResultCode(
        code="700.100.700",
        name="REFERENCED_TRANSACTION_IS_OF_INAPPROPRIATE_TYPE",
        description="referenced transaction is of inappropriate type",
    )
    REFERENCED_A_DB_TRANSACTION_WITHOUT_EXPLICITLY_PROVIDING_AN_ACCOUNT_NOT_ALLOWED_TO_USED_REFERENCED_ACCOUNT = (
        ResultCode(  # noqa: E501
            code="700.100.701",
            name="REFERENCED_A_DB_TRANSACTION_WITHOUT_EXPLICITLY_PROVIDING_AN_ACCOUNT_NOT_"
            "ALLOWED_TO_USED_REFERENCED_ACCOUNT",
            description="referenced a DB transaction without explicitly providing an account. "
            "Not allowed to used referenced account.",
        )
    )
    CROSS_LINKAGE_OF_TWO_TRANSACTION_TREES = ResultCode(
        code="700.100.710",
        name="CROSS_LINKAGE_OF_TWO_TRANSACTION_TREES",
        description="cross-linkage of two transaction-trees",
    )
    REFERENCED_TX_CAN_NOT_BE_REFUNDED_CAPTURED_OR_REVERSED_INVALID_TYPE = ResultCode(
        code="700.300.100",
        name="REFERENCED_TX_CAN_NOT_BE_REFUNDED_CAPTURED_OR_REVERSED_INVALID_TYPE",
        description="referenced tx can not be refunded, captured or reversed (invalid type)",
    )
    REFERENCED_TX_WAS_REJECTED = ResultCode(
        code="700.300.200", name="REFERENCED_TX_WAS_REJECTED", description="referenced tx was rejected"
    )
    REFERENCED_TX_CAN_NOT_BE_REFUNDED_CAPTURED_OR_REVERSED_ALREADY_REFUNDED_CAPTURED_OR_REVERSED = ResultCode(
        code="700.300.300",
        name="REFERENCED_TX_CAN_NOT_BE_REFUNDED_CAPTURED_OR_REVERSED_ALREADY_REFUNDED_CAPTURED_OR_REVERSED",
        description="referenced tx can not be refunded, captured or reversed (already refunded, captured or reversed)",
    )
    REFERENCED_TX_CAN_NOT_BE_CAPTURED_CUT_OFF_TIME_REACHED = ResultCode(
        code="700.300.400",
        name="REFERENCED_TX_CAN_NOT_BE_CAPTURED_CUT_OFF_TIME_REACHED",
        description="referenced tx can not be captured (cut off time reached)",
    )
    CHARGEBACK_ERROR_MULTIPLE_CHARGEBACKS = ResultCode(
        code="700.300.500",
        name="CHARGEBACK_ERROR_MULTIPLE_CHARGEBACKS",
        description="chargeback error (multiple chargebacks)",
    )
    REFERENCED_TX_CAN_NOT_BE_REFUNDED_OR_REVERSED_WAS_CHARGEBACKED = ResultCode(
        code="700.300.600",
        name="REFERENCED_TX_CAN_NOT_BE_REFUNDED_OR_REVERSED_WAS_CHARGEBACKED",
        description="referenced tx can not be refunded or reversed (was chargebacked)",
    )
    REFERENCED_TX_CAN_NOT_BE_REVERSED_REVERSAL_NOT_POSSIBLE_ANYMORE = ResultCode(
        code="700.300.700",
        name="REFERENCED_TX_CAN_NOT_BE_REVERSED_REVERSAL_NOT_POSSIBLE_ANYMORE",
        description="referenced tx can not be reversed (reversal not possible anymore)",
    )
    REFERENCED_TX_CAN_NOT_BE_VOIDED = ResultCode(
        code="700.300.800", name="REFERENCED_TX_CAN_NOT_BE_VOIDED", description="referenced tx can not be voided"
    )
    SERIOUS_WORKFLOW_ERROR_CALL_SUPPORT = ResultCode(
        code="700.400.000",
        name="SERIOUS_WORKFLOW_ERROR_CALL_SUPPORT",
        description="serious workflow error (call support)",
    )
    CANNOT_CAPTURE_PA_VALUE_EXCEEDED_PA_REVERTED_OR_INVALID_WORKFLOW = ResultCode(
        code="700.400.100",
        name="CANNOT_CAPTURE_PA_VALUE_EXCEEDED_PA_REVERTED_OR_INVALID_WORKFLOW",
        description="cannot capture (PA value exceeded, PA reverted or invalid workflow?)",
    )
    CANNOT_CAPTURE_NOT_SUPPORTED_BY_AUTHORIZATION_SYSTEM = ResultCode(
        code="700.400.101",
        name="CANNOT_CAPTURE_NOT_SUPPORTED_BY_AUTHORIZATION_SYSTEM",
        description="cannot capture (Not supported by authorization system)",
    )
    CANNOT_REFUND_REFUND_VOLUME_EXCEEDED_OR_TX_REVERSED_OR_INVALID_WORKFLOW = ResultCode(
        code="700.400.200",
        name="CANNOT_REFUND_REFUND_VOLUME_EXCEEDED_OR_TX_REVERSED_OR_INVALID_WORKFLOW",
        description="cannot refund (refund volume exceeded or tx reversed or invalid workflow?)",
    )
    CANNOT_REVERSE_ALREADY_REFUNDED_REVERSED_INVALID_WORKFLOW_OR_AMOUNT_EXCEEDED = ResultCode(
        code="700.400.300",
        name="CANNOT_REVERSE_ALREADY_REFUNDED_REVERSED_INVALID_WORKFLOW_OR_AMOUNT_EXCEEDED",
        description="cannot reverse (already refunded|reversed, invalid workflow or amount exceeded)",
    )
    CANNOT_CHARGEBACK_ALREADY_CHARGEBACKED_OR_INVALID_WORKFLOW = ResultCode(
        code="700.400.400",
        name="CANNOT_CHARGEBACK_ALREADY_CHARGEBACKED_OR_INVALID_WORKFLOW",
        description="cannot chargeback (already chargebacked or invalid workflow?)",
    )
    CHARGEBACK_CAN_ONLY_BE_GENERATED_INTERNALLY_BY_THE_PAYMENT_SYSTEM = ResultCode(
        code="700.400.402",
        name="CHARGEBACK_CAN_ONLY_BE_GENERATED_INTERNALLY_BY_THE_PAYMENT_SYSTEM",
        description="chargeback can only be generated internally by the payment system",
    )
    CANNOT_REVERSAL_CHARGEBACK_CHARGEBACK_IS_ALREADY_REVERSALED_OR_INVALID_WORKFLOW = ResultCode(
        code="700.400.410",
        name="CANNOT_REVERSAL_CHARGEBACK_CHARGEBACK_IS_ALREADY_REVERSALED_OR_INVALID_WORKFLOW",
        description="cannot reversal chargeback (chargeback is already reversaled or invalid workflow?)",
    )
    CANNOT_REVERSE_CHARGEBACK_OR_INVALID_WORKFLOW_SECOND_CHARGEBACK = ResultCode(
        code="700.400.411",
        name="CANNOT_REVERSE_CHARGEBACK_OR_INVALID_WORKFLOW_SECOND_CHARGEBACK",
        description="cannot reverse chargeback or invalid workflow (second chargeback)",
    )
    CANNOT_REVERSAL_CHARGEBACK_NO_CHARGEBACK_EXISTING_OR_INVALID_WORKFLOW = ResultCode(
        code="700.400.420",
        name="CANNOT_REVERSAL_CHARGEBACK_NO_CHARGEBACK_EXISTING_OR_INVALID_WORKFLOW",
        description="cannot reversal chargeback (no chargeback existing or invalid workflow?)",
    )
    CAPTURE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA = ResultCode(
        code="700.400.510",
        name="CAPTURE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA",
        description="capture needs at least one successful transaction of type (PA)",
    )
    REFUND_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB_OR_RC = ResultCode(
        code="700.400.520",
        name="REFUND_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB_OR_RC",
        description="refund needs at least one successful transaction of type (CP or DB or RB or RC)",
    )
    REVERSAL_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB_OR_PA = ResultCode(
        code="700.400.530",
        name="REVERSAL_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB_OR_PA",
        description="reversal needs at least one successful transaction of type (CP or DB or RB or PA)",
    )
    RECONCEILE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB = ResultCode(
        code="700.400.540",
        name="RECONCEILE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB",
        description="reconceile needs at least one successful transaction of type (CP or DB or RB)",
    )
    CHARGEBACK_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB = ResultCode(
        code="700.400.550",
        name="CHARGEBACK_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_CP_OR_DB_OR_RB",
        description="chargeback needs at least one successful transaction of type (CP or DB or RB)",
    )
    RECEIPT_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA_OR_CP_OR_DB_OR_RB = ResultCode(
        code="700.400.560",
        name="RECEIPT_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA_OR_CP_OR_DB_OR_RB",
        description="receipt needs at least one successful transaction of type (PA or CP or DB or RB)",
    )
    RECEIPT_ON_A_REGISTRATION_NEEDS_A_SUCCESSFULL_REGISTRATION_IN_STATE_OPEN = ResultCode(
        code="700.400.561",
        name="RECEIPT_ON_A_REGISTRATION_NEEDS_A_SUCCESSFULL_REGISTRATION_IN_STATE_OPEN",
        description="receipt on a registration needs a successfull registration in state 'OPEN'",
    )
    RECEIPTS_ARE_CONFIGURED_TO_BE_GENERATED_ONLY_INTERNALLY_BY_THE_PAYMENT_SYSTEM = ResultCode(
        code="700.400.562",
        name="RECEIPTS_ARE_CONFIGURED_TO_BE_GENERATED_ONLY_INTERNALLY_BY_THE_PAYMENT_SYSTEM",
        description="receipts are configured to be generated only internally by the payment system",
    )
    FINALIZE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA_OR_DB = ResultCode(
        code="700.400.565",
        name="FINALIZE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_PA_OR_DB",
        description="finalize needs at least one successful transaction of type (PA or DB)",
    )
    CANNOT_REFERENCE_A_WAITING_PENDING_TRANSACTION = ResultCode(
        code="700.400.570",
        name="CANNOT_REFERENCE_A_WAITING_PENDING_TRANSACTION",
        description="cannot reference a waiting/pending transaction",
    )
    CANNOT_FIND_TRANSACTION = ResultCode(
        code="700.400.580", name="CANNOT_FIND_TRANSACTION", description="cannot find transaction"
    )
    INSTALLMENT_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_DB_OR_PA = ResultCode(
        code="700.400.590",
        name="INSTALLMENT_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_DB_OR_PA",
        description="installment needs at least one successful transaction of type (DB or PA)",
    )
    FINALIZE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_IN_DB_PA_OR_CD = ResultCode(
        code="700.400.600",
        name="FINALIZE_NEEDS_AT_LEAST_ONE_SUCCESSFUL_TRANSACTION_OF_TYPE_IN_DB_PA_OR_CD",
        description="finalize needs at least one successful transaction of type (IN, DB, PA or CD)",
    )
    INITIAL_AND_REFERENCING_CHANNEL_IDS_DO_NOT_MATCH = ResultCode(
        code="700.400.700",
        name="INITIAL_AND_REFERENCING_CHANNEL_IDS_DO_NOT_MATCH",
        description="initial and referencing channel-ids do not match",
    )
    CANNOT_TRANSFER_MONEY_FROM_ONE_ACCOUNT_TO_THE_SAME_ACCOUNT = ResultCode(
        code="700.450.001",
        name="CANNOT_TRANSFER_MONEY_FROM_ONE_ACCOUNT_TO_THE_SAME_ACCOUNT",
        description="cannot transfer money from one account to the same account",
    )
    REFERENCED_SESSION_CONTAINS_TOO_MANY_TRANSACTIONS = ResultCode(
        code="700.500.001",
        name="REFERENCED_SESSION_CONTAINS_TOO_MANY_TRANSACTIONS",
        description="referenced session contains too many transactions",
    )
    CAPTURE_OR_PREAUTHORIZATION_APPEARS_TOO_LATE_IN_REFERENCED_SESSION = ResultCode(
        code="700.500.002",
        name="CAPTURE_OR_PREAUTHORIZATION_APPEARS_TOO_LATE_IN_REFERENCED_SESSION",
        description="capture or preauthorization appears too late in referenced session",
    )
    TEST_ACCOUNTS_NOT_ALLOWED_IN_PRODUCTION = ResultCode(
        code="700.500.003",
        name="TEST_ACCOUNTS_NOT_ALLOWED_IN_PRODUCTION",
        description="test accounts not allowed in production",
    )
    CANNOT_REFER_A_TRANSACTION_WHICH_CONTAINS_DELETED_CUSTOMER_INFORMATION = ResultCode(
        code="700.500.004",
        name="CANNOT_REFER_A_TRANSACTION_WHICH_CONTAINS_DELETED_CUSTOMER_INFORMATION",
        description="cannot refer a transaction which contains deleted customer information",
    )
    TRANSACTION_DECLINED_FOR_UNKNOWN_REASON = ResultCode(
        code="800.100.100",
        name="TRANSACTION_DECLINED_FOR_UNKNOWN_REASON",
        description="transaction declined for unknown reason",
    )
    TRANSACTION_DECLINED_REFUND_ON_GAMBLING_TX_NOT_ALLOWED = ResultCode(
        code="800.100.150",
        name="TRANSACTION_DECLINED_REFUND_ON_GAMBLING_TX_NOT_ALLOWED",
        description="transaction declined (refund on gambling tx not allowed)",
    )
    TRANSACTION_DECLINED_INVALID_CARD_2 = ResultCode(
        code="800.100.151",
        name="TRANSACTION_DECLINED_INVALID_CARD_2",
        description="transaction declined (invalid card)",
    )
    TRANSACTION_DECLINED_BY_AUTHORIZATION_SYSTEM = ResultCode(
        code="800.100.152",
        name="TRANSACTION_DECLINED_BY_AUTHORIZATION_SYSTEM",
        description="transaction declined by authorization system",
    )
    TRANSACTION_DECLINED_INVALID_CVV = ResultCode(
        code="800.100.153", name="TRANSACTION_DECLINED_INVALID_CVV", description="transaction declined (invalid CVV)"
    )
    TRANSACTION_DECLINED_TRANSACTION_MARKED_AS_INVALID = ResultCode(
        code="800.100.154",
        name="TRANSACTION_DECLINED_TRANSACTION_MARKED_AS_INVALID",
        description="transaction declined (transaction marked as invalid)",
    )
    TRANSACTION_DECLINED_AMOUNT_EXCEEDS_CREDIT = ResultCode(
        code="800.100.155",
        name="TRANSACTION_DECLINED_AMOUNT_EXCEEDS_CREDIT",
        description="transaction declined (amount exceeds credit)",
    )
    TRANSACTION_DECLINED_FORMAT_ERROR_2 = ResultCode(
        code="800.100.156",
        name="TRANSACTION_DECLINED_FORMAT_ERROR_2",
        description="transaction declined (format error)",
    )
    TRANSACTION_DECLINED_WRONG_EXPIRY_DATE = ResultCode(
        code="800.100.157",
        name="TRANSACTION_DECLINED_WRONG_EXPIRY_DATE",
        description="transaction declined (wrong expiry date)",
    )
    TRANSACTION_DECLINED_SUSPECTING_MANIPULATION = ResultCode(
        code="800.100.158",
        name="TRANSACTION_DECLINED_SUSPECTING_MANIPULATION",
        description="transaction declined (suspecting manipulation)",
    )
    TRANSACTION_DECLINED_STOLEN_CARD = ResultCode(
        code="800.100.159", name="TRANSACTION_DECLINED_STOLEN_CARD", description="transaction declined (stolen card)"
    )
    TRANSACTION_DECLINED_CARD_BLOCKED = ResultCode(
        code="800.100.160", name="TRANSACTION_DECLINED_CARD_BLOCKED", description="transaction declined (card blocked)"
    )
    TRANSACTION_DECLINED_TOO_MANY_INVALID_TRIES = ResultCode(
        code="800.100.161",
        name="TRANSACTION_DECLINED_TOO_MANY_INVALID_TRIES",
        description="transaction declined (too many invalid tries)",
    )
    TRANSACTION_DECLINED_LIMIT_EXCEEDED = ResultCode(
        code="800.100.162",
        name="TRANSACTION_DECLINED_LIMIT_EXCEEDED",
        description="transaction declined (limit exceeded)",
    )
    TRANSACTION_DECLINED_MAXIMUM_TRANSACTION_FREQUENCY_EXCEEDED = ResultCode(
        code="800.100.163",
        name="TRANSACTION_DECLINED_MAXIMUM_TRANSACTION_FREQUENCY_EXCEEDED",
        description="transaction declined (maximum transaction frequency exceeded)",
    )
    TRANSACTION_DECLINED_MERCHANTS_LIMIT_EXCEEDED = ResultCode(
        code="800.100.164",
        name="TRANSACTION_DECLINED_MERCHANTS_LIMIT_EXCEEDED",
        description="transaction declined (merchants limit exceeded)",
    )
    TRANSACTION_DECLINED_CARD_LOST = ResultCode(
        code="800.100.165", name="TRANSACTION_DECLINED_CARD_LOST", description="transaction declined (card lost)"
    )
    TRANSACTION_DECLINED_INCORRECT_PERSONAL_IDENTIFICATION_NUMBER = ResultCode(
        code="800.100.166",
        name="TRANSACTION_DECLINED_INCORRECT_PERSONAL_IDENTIFICATION_NUMBER",
        description="transaction declined (Incorrect personal identification number)",
    )
    TRANSACTION_DECLINED_REFERENCING_TRANSACTION_DOES_NOT_MATCH = ResultCode(
        code="800.100.167",
        name="TRANSACTION_DECLINED_REFERENCING_TRANSACTION_DOES_NOT_MATCH",
        description="transaction declined (referencing transaction does not match)",
    )
    TRANSACTION_DECLINED_RESTRICTED_CARD = ResultCode(
        code="800.100.168",
        name="TRANSACTION_DECLINED_RESTRICTED_CARD",
        description="transaction declined (restricted card)",
    )
    TRANSACTION_DECLINED_CARD_TYPE_IS_NOT_PROCESSED_BY_THE_AUTHORIZATION_CENTER = ResultCode(
        code="800.100.169",
        name="TRANSACTION_DECLINED_CARD_TYPE_IS_NOT_PROCESSED_BY_THE_AUTHORIZATION_CENTER",
        description="transaction declined (card type is not processed by the authorization center)",
    )
    TRANSACTION_DECLINED_TRANSACTION_NOT_PERMITTED = ResultCode(
        code="800.100.170",
        name="TRANSACTION_DECLINED_TRANSACTION_NOT_PERMITTED",
        description="transaction declined (transaction not permitted)",
    )
    TRANSACTION_DECLINED_PICK_UP_CARD = ResultCode(
        code="800.100.171", name="TRANSACTION_DECLINED_PICK_UP_CARD", description="transaction declined (pick up card)"
    )
    TRANSACTION_DECLINED_ACCOUNT_BLOCKED = ResultCode(
        code="800.100.172",
        name="TRANSACTION_DECLINED_ACCOUNT_BLOCKED",
        description="transaction declined (account blocked)",
    )
    TRANSACTION_DECLINED_INVALID_CURRENCY_NOT_PROCESSED_BY_AUTHORIZATION_CENTER = ResultCode(
        code="800.100.173",
        name="TRANSACTION_DECLINED_INVALID_CURRENCY_NOT_PROCESSED_BY_AUTHORIZATION_CENTER",
        description="transaction declined (invalid currency, not processed by authorization center)",
    )
    TRANSACTION_DECLINED_INVALID_AMOUNT = ResultCode(
        code="800.100.174",
        name="TRANSACTION_DECLINED_INVALID_AMOUNT",
        description="transaction declined (invalid amount)",
    )
    TRANSACTION_DECLINED_INVALID_BRAND = ResultCode(
        code="800.100.175",
        name="TRANSACTION_DECLINED_INVALID_BRAND",
        description="transaction declined (invalid brand)",
    )
    TRANSACTION_DECLINED_ACCOUNT_TEMPORARILY_NOT_AVAILABLE_PLEASE_TRY_AGAIN_LATER = ResultCode(
        code="800.100.176",
        name="TRANSACTION_DECLINED_ACCOUNT_TEMPORARILY_NOT_AVAILABLE_PLEASE_TRY_AGAIN_LATER",
        description="transaction declined (account temporarily not available. Please try again later)",
    )
    TRANSACTION_DECLINED_AMOUNT_FIELD_SHOULD_NOT_BE_EMPTY = ResultCode(
        code="800.100.177",
        name="TRANSACTION_DECLINED_AMOUNT_FIELD_SHOULD_NOT_BE_EMPTY",
        description="transaction declined (amount field should not be empty)",
    )
    TRANSACTION_DECLINED_PIN_ENTERED_INCORRECTLY_TOO_OFTEN = ResultCode(
        code="800.100.178",
        name="TRANSACTION_DECLINED_PIN_ENTERED_INCORRECTLY_TOO_OFTEN",
        description="transaction declined (PIN entered incorrectly too often)",
    )
    TRANSACTION_DECLINED_EXCEEDS_WITHDRAWAL_COUNT_LIMIT = ResultCode(
        code="800.100.179",
        name="TRANSACTION_DECLINED_EXCEEDS_WITHDRAWAL_COUNT_LIMIT",
        description="transaction declined (exceeds withdrawal count limit)",
    )
    TRANSACTION_DECLINED_INVALID_CONFIGURATION_DATA_2 = ResultCode(
        code="800.100.190",
        name="TRANSACTION_DECLINED_INVALID_CONFIGURATION_DATA_2",
        description="transaction declined (invalid configuration data)",
    )
    TRANSACTION_DECLINED_TRANSACTION_IN_WRONG_STATE_ON_AQUIRER_SIDE = ResultCode(
        code="800.100.191",
        name="TRANSACTION_DECLINED_TRANSACTION_IN_WRONG_STATE_ON_AQUIRER_SIDE",
        description="transaction declined (transaction in wrong state on aquirer side)",
    )
    TRANSACTION_DECLINED_INVALID_CVV_AMOUNT_HAS_STILL_BEEN_RESERVED_ON_THE_CUSTOMERS_CARD_AND_WILL_BE_RELEASED_IN_A_FEW_BUSINESS_DAYS_PLEASE_ENSURE_THE_CVV_CODE_IS_ACCURATE_BEFORE_RETRYING_THE_TRANSACTION = ResultCode(  # noqa: E501
        code="800.100.192",
        name="TRANSACTION_DECLINED_INVALID_CVV_AMOUNT_HAS_STILL_BEEN_RESERVED_ON_THE_CUSTOMERS_CARD_AND_WILL_BE_"
        "RELEASED_IN_A_FEW_BUSINESS_DAYS_PLEASE_ENSURE_THE_CVV_CODE_IS_ACCURATE_BEFORE_RETRYING_THE_TRANSACTION",
        description="transaction declined (invalid CVV, Amount has still been reserved on the customer's card and "
        "will be released in a few business days. Please ensure the CVV code is accurate "
        "before retrying the transaction)",
    )
    TRANSACTION_DECLINED_USERACCOUNT_NUMBER_ID_UNKNOWN = ResultCode(
        code="800.100.195",
        name="TRANSACTION_DECLINED_USERACCOUNT_NUMBER_ID_UNKNOWN",
        description="transaction declined (UserAccount Number/ID unknown)",
    )
    TRANSACTION_DECLINED_REGISTRATION_ERROR = ResultCode(
        code="800.100.196",
        name="TRANSACTION_DECLINED_REGISTRATION_ERROR",
        description="transaction declined (registration error)",
    )
    TRANSACTION_DECLINED_REGISTRATION_CANCELLED_EXTERNALLY = ResultCode(
        code="800.100.197",
        name="TRANSACTION_DECLINED_REGISTRATION_CANCELLED_EXTERNALLY",
        description="transaction declined (registration cancelled externally)",
    )
    TRANSACTION_DECLINED_INVALID_HOLDER = ResultCode(
        code="800.100.198",
        name="TRANSACTION_DECLINED_INVALID_HOLDER",
        description="transaction declined (invalid holder)",
    )
    TRANSACTION_DECLINED_INVALID_TAX_NUMBER = ResultCode(
        code="800.100.199",
        name="TRANSACTION_DECLINED_INVALID_TAX_NUMBER",
        description="transaction declined (invalid tax number)",
    )
    REFER_TO_PAYER_DUE_TO_REASON_NOT_SPECIFIED = ResultCode(
        code="800.100.200",
        name="REFER_TO_PAYER_DUE_TO_REASON_NOT_SPECIFIED",
        description="Refer to Payer due to reason not specified",
    )
    ACCOUNT_OR_BANK_DETAILS_INCORRECT_2 = ResultCode(
        code="800.100.201", name="ACCOUNT_OR_BANK_DETAILS_INCORRECT_2", description="Account or Bank Details Incorrect"
    )
    ACCOUNT_CLOSED_2 = ResultCode(code="800.100.202", name="ACCOUNT_CLOSED_2", description="Account Closed")
    INSUFFICIENT_FUNDS_2 = ResultCode(code="800.100.203", name="INSUFFICIENT_FUNDS_2", description="Insufficient Funds")
    MANDATE_EXPIRED = ResultCode(code="800.100.204", name="MANDATE_EXPIRED", description="Mandate Expired")
    MANDATE_DISCARDED = ResultCode(code="800.100.205", name="MANDATE_DISCARDED", description="Mandate Discarded")
    REFUND_OF_AN_AUTHORIZED_PAYMENT_REQUESTED_BY_THE_CUSTOMER = ResultCode(
        code="800.100.206",
        name="REFUND_OF_AN_AUTHORIZED_PAYMENT_REQUESTED_BY_THE_CUSTOMER",
        description="Refund of an authorized payment requested by the customer",
    )
    REFUND_REQUESTED = ResultCode(code="800.100.207", name="REFUND_REQUESTED", description="Refund requested")
    DIRECT_DEBIT_NOT_ENABLED_FOR_THE_SPECIFIED_ACCOUNT_OR_BANK = ResultCode(
        code="800.100.208",
        name="DIRECT_DEBIT_NOT_ENABLED_FOR_THE_SPECIFIED_ACCOUNT_OR_BANK",
        description="Direct debit not enabled for the specified account or bank",
    )
    CC_BANK_ACCOUNT_HOLDER_NOT_VALID_2 = ResultCode(
        code="800.100.402", name="CC_BANK_ACCOUNT_HOLDER_NOT_VALID_2", description="cc/bank account holder not valid"
    )
    TRANSACTION_DECLINED_REVOCATION_OF_AUTHORISATION_ORDER = ResultCode(
        code="800.100.403",
        name="TRANSACTION_DECLINED_REVOCATION_OF_AUTHORISATION_ORDER",
        description="transaction declined (revocation of authorisation order)",
    )
    CARD_HOLDER_HAS_ADVISED_HIS_BANK_TO_STOP_THIS_RECURRING_PAYMENT = ResultCode(
        code="800.100.500",
        name="CARD_HOLDER_HAS_ADVISED_HIS_BANK_TO_STOP_THIS_RECURRING_PAYMENT",
        description="Card holder has advised his bank to stop this recurring payment",
    )
    CARD_HOLDER_HAS_ADVISED_HIS_BANK_TO_STOP_ALL_RECURRING_PAYMENTS_FOR_THIS_MERCHANT = ResultCode(
        code="800.100.501",
        name="CARD_HOLDER_HAS_ADVISED_HIS_BANK_TO_STOP_ALL_RECURRING_PAYMENTS_FOR_THIS_MERCHANT",
        description="Card holder has advised his bank to stop all recurring payments for this merchant",
    )
    DUPLICATE_TRANSACTION = ResultCode(
        code="800.110.100", name="DUPLICATE_TRANSACTION", description="duplicate transaction"
    )
    REJECTED_BY_THROTTLING = ResultCode(
        code="800.120.100", name="REJECTED_BY_THROTTLING", description="Rejected by Throttling."
    )
    MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_ACCOUNT_ALREADY_EXCEEDED = ResultCode(
        code="800.120.101",
        name="MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_ACCOUNT_ALREADY_EXCEEDED",
        description="maximum number of transactions per account already exceeded",
    )
    MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_IP_ALREADY_EXCEEDED = ResultCode(
        code="800.120.102",
        name="MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_IP_ALREADY_EXCEEDED",
        description="maximum number of transactions per ip already exceeded",
    )
    MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_EMAIL_ALREADY_EXCEEDED = ResultCode(
        code="800.120.103",
        name="MAXIMUM_NUMBER_OF_TRANSACTIONS_PER_EMAIL_ALREADY_EXCEEDED",
        description="maximum number of transactions per email already exceeded",
    )
    MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_ALREADY_EXCEEDED = ResultCode(
        code="800.120.200",
        name="MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_ALREADY_EXCEEDED",
        description="maximum total volume of transactions already exceeded",
    )
    MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_ACCOUNT_ALREADY_EXCEEDED = ResultCode(
        code="800.120.201",
        name="MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_ACCOUNT_ALREADY_EXCEEDED",
        description="maximum total volume of transactions per account already exceeded",
    )
    MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_IP_ALREADY_EXCEEDED = ResultCode(
        code="800.120.202",
        name="MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_IP_ALREADY_EXCEEDED",
        description="maximum total volume of transactions per ip already exceeded",
    )
    MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_EMAIL_ALREADY_EXCEEDED = ResultCode(
        code="800.120.203",
        name="MAXIMUM_TOTAL_VOLUME_OF_TRANSACTIONS_PER_EMAIL_ALREADY_EXCEEDED",
        description="maximum total volume of transactions per email already exceeded",
    )
    CHARGEBACK_RATE_PER_BIN_EXCEEDED = ResultCode(
        code="800.120.300", name="CHARGEBACK_RATE_PER_BIN_EXCEEDED", description="chargeback rate per bin exceeded"
    )
    MAXIMUM_NUMBER_OF_TRANSACTIONS_OR_TOTAL_VOLUME_FOR_CONFIGURED_MIDS_OR_CIS_EXCEEDED = ResultCode(
        code="800.120.401",
        name="MAXIMUM_NUMBER_OF_TRANSACTIONS_OR_TOTAL_VOLUME_FOR_CONFIGURED_MIDS_OR_CIS_EXCEEDED",
        description="maximum number of transactions or total volume for configured MIDs or CIs exceeded",
    )
    CHANNEL_NOT_CONFIGURED_FOR_GIVEN_SOURCE_TYPE_PLEASE_CONTACT_YOUR_ACCOUNT_MANAGER = ResultCode(
        code="800.121.100",
        name="CHANNEL_NOT_CONFIGURED_FOR_GIVEN_SOURCE_TYPE_PLEASE_CONTACT_YOUR_ACCOUNT_MANAGER",
        description="Channel not configured for given source type. Please contact your account manager.",
    )
    SECURE_QUERY_IS_NOT_ENABLED_FOR_THIS_ENTITY_PLEASE_CONTACT_YOUR_ACCOUNT_MANAGER = ResultCode(
        code="800.121.200",
        name="SECURE_QUERY_IS_NOT_ENABLED_FOR_THIS_ENTITY_PLEASE_CONTACT_YOUR_ACCOUNT_MANAGER",
        description="Secure Query is not enabled for this entity. Please contact your account manager.",
    )
    TRANSACTION_WITH_SAME_TRANSACTIONID_ALREADY_EXISTS = ResultCode(
        code="800.130.100",
        name="TRANSACTION_WITH_SAME_TRANSACTIONID_ALREADY_EXISTS",
        description="Transaction with same TransactionId already exists",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_PER_MOBILE_NUMBER_EXCEEDED = ResultCode(
        code="800.140.100",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_PER_MOBILE_NUMBER_EXCEEDED",
        description="maximum number of registrations per mobile number exceeded",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_PER_EMAIL_ADDRESS_EXCEEDED = ResultCode(
        code="800.140.101",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_PER_EMAIL_ADDRESS_EXCEEDED",
        description="maximum number of registrations per email address exceeded",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_MOBILE_PER_CREDIT_CARD_NUMBER_EXCEEDED = ResultCode(
        code="800.140.110",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_MOBILE_PER_CREDIT_CARD_NUMBER_EXCEEDED",
        description="maximum number of registrations of mobile per credit card number exceeded",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_CREDIT_CARD_NUMBER_PER_MOBILE_EXCEEDED = ResultCode(
        code="800.140.111",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_CREDIT_CARD_NUMBER_PER_MOBILE_EXCEEDED",
        description="maximum number of registrations of credit card number per mobile exceeded",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_EMAIL_PER_CREDIT_CARD_NUMBER_EXCEEDED = ResultCode(
        code="800.140.112",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_EMAIL_PER_CREDIT_CARD_NUMBER_EXCEEDED",
        description="maximum number of registrations of email per credit card number exceeded",
    )
    MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_CREDIT_CARD_NUMBER_PER_EMAIL_EXCEEDED = ResultCode(
        code="800.140.113",
        name="MAXIMUM_NUMBER_OF_REGISTRATIONS_OF_CREDIT_CARD_NUMBER_PER_EMAIL_EXCEEDED",
        description="maximum number of registrations of credit card number per email exceeded",
    )
    ACCOUNT_HOLDER_DOES_NOT_MATCH_CUSTOMER_NAME = ResultCode(
        code="800.150.100",
        name="ACCOUNT_HOLDER_DOES_NOT_MATCH_CUSTOMER_NAME",
        description="Account Holder does not match Customer Name",
    )
    INVALID_PAYMENT_DATA_FOR_CONFIGURED_SHOPPER_DISPATCHING_TYPE = ResultCode(
        code="800.160.100",
        name="INVALID_PAYMENT_DATA_FOR_CONFIGURED_SHOPPER_DISPATCHING_TYPE",
        description="Invalid payment data for configured Shopper Dispatching Type",
    )
    INVALID_PAYMENT_DATA_FOR_CONFIGURED_PAYMENT_DISPATCHING_TYPE = ResultCode(
        code="800.160.110",
        name="INVALID_PAYMENT_DATA_FOR_CONFIGURED_PAYMENT_DISPATCHING_TYPE",
        description="Invalid payment data for configured Payment Dispatching Type",
    )
    INVALID_PAYMENT_DATA_FOR_CONFIGURED_RECURRING_TRANSACTION_DISPATCHING_TYPE = ResultCode(
        code="800.160.120",
        name="INVALID_PAYMENT_DATA_FOR_CONFIGURED_RECURRING_TRANSACTION_DISPATCHING_TYPE",
        description="Invalid payment data for configured Recurring Transaction Dispatching Type",
    )
    INVALID_PAYMENT_DATA_FOR_CONFIGURED_TICKETSIZE_DISPATCHING_TYPE = ResultCode(
        code="800.160.130",
        name="INVALID_PAYMENT_DATA_FOR_CONFIGURED_TICKETSIZE_DISPATCHING_TYPE",
        description="Invalid payment data for configured TicketSize Dispatching Type",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_STOLEN = ResultCode(
        code="800.200.159",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_STOLEN",
        description="account or user is blacklisted (card stolen)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_BLOCKED = ResultCode(
        code="800.200.160",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_BLOCKED",
        description="account or user is blacklisted (card blocked)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_LOST = ResultCode(
        code="800.200.165",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_CARD_LOST",
        description="account or user is blacklisted (card lost)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_ACCOUNT_CLOSED = ResultCode(
        code="800.200.202",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_ACCOUNT_CLOSED",
        description="account or user is blacklisted (account closed)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_ACCOUNT_BLOCKED = ResultCode(
        code="800.200.208",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_ACCOUNT_BLOCKED",
        description="account or user is blacklisted (account blocked)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED_FRAUDULENT_TRANSACTION = ResultCode(
        code="800.200.220",
        name="ACCOUNT_OR_USER_IS_BLACKLISTED_FRAUDULENT_TRANSACTION",
        description="account or user is blacklisted (fraudulent transaction)",
    )
    ACCOUNT_OR_USER_IS_BLACKLISTED = ResultCode(
        code="800.300.101", name="ACCOUNT_OR_USER_IS_BLACKLISTED", description="account or user is blacklisted"
    )
    COUNTRY_BLACKLISTED = ResultCode(code="800.300.102", name="COUNTRY_BLACKLISTED", description="country blacklisted")
    EMAIL_IS_BLACKLISTED = ResultCode(
        code="800.300.200", name="EMAIL_IS_BLACKLISTED", description="email is blacklisted"
    )
    IP_BLACKLISTED = ResultCode(code="800.300.301", name="IP_BLACKLISTED", description="ip blacklisted")
    IP_IS_ANONYMOUS_PROXY = ResultCode(
        code="800.300.302", name="IP_IS_ANONYMOUS_PROXY", description="ip is anonymous proxy"
    )
    BIN_BLACKLISTED = ResultCode(code="800.300.401", name="BIN_BLACKLISTED", description="bin blacklisted")
    TRANSACTION_TEMPORARY_BLACKLISTED_TOO_MANY_TRIES_INVALID_CVV = ResultCode(
        code="800.300.500",
        name="TRANSACTION_TEMPORARY_BLACKLISTED_TOO_MANY_TRIES_INVALID_CVV",
        description="transaction temporary blacklisted (too many tries invalid CVV)",
    )
    TRANSACTION_TEMPORARY_BLACKLISTED_TOO_MANY_TRIES_INVALID_EXPIRE_DATE = ResultCode(
        code="800.300.501",
        name="TRANSACTION_TEMPORARY_BLACKLISTED_TOO_MANY_TRIES_INVALID_EXPIRE_DATE",
        description="transaction temporary blacklisted (too many tries invalid expire date)",
    )
    ACCOUNT_CLOSED_3 = ResultCode(code="800.310.200", name="ACCOUNT_CLOSED_3", description="Account closed")
    ACCOUNT_NOT_FOUND = ResultCode(code="800.310.210", name="ACCOUNT_NOT_FOUND", description="Account not found")
    ACCOUNT_NOT_FOUND_BIN_ISSUER_NOT_PARTICIPATING = ResultCode(
        code="800.310.211",
        name="ACCOUNT_NOT_FOUND_BIN_ISSUER_NOT_PARTICIPATING",
        description="Account not found (BIN/issuer not participating)",
    )
    AVS_CHECK_FAILED = ResultCode(code="800.400.100", name="AVS_CHECK_FAILED", description="AVS Check Failed")
    MISMATCH_OF_AVS_STREET_VALUE = ResultCode(
        code="800.400.101", name="MISMATCH_OF_AVS_STREET_VALUE", description="Mismatch of AVS street value"
    )
    MISMATCH_OF_AVS_STREET_NUMBER = ResultCode(
        code="800.400.102", name="MISMATCH_OF_AVS_STREET_NUMBER", description="Mismatch of AVS street number"
    )
    MISMATCH_OF_AVS_PO_BOX_VALUE_FATAL = ResultCode(
        code="800.400.103", name="MISMATCH_OF_AVS_PO_BOX_VALUE_FATAL", description="Mismatch of AVS PO box value fatal"
    )
    MISMATCH_OF_AVS_ZIP_CODE_VALUE_FATAL = ResultCode(
        code="800.400.104",
        name="MISMATCH_OF_AVS_ZIP_CODE_VALUE_FATAL",
        description="Mismatch of AVS zip code value fatal",
    )
    MISMATCH_OF_AVS_SETTINGS_AVSKIP_AVIGNORE_AVSREJECTPOLICY_VALUE = ResultCode(
        code="800.400.105",
        name="MISMATCH_OF_AVS_SETTINGS_AVSKIP_AVIGNORE_AVSREJECTPOLICY_VALUE",
        description="Mismatch of AVS settings (AVSkip, AVIgnore, AVSRejectPolicy) value",
    )
    AVS_CHECK_FAILED_AMOUNT_HAS_STILL_BEEN_RESERVED_ON_THE_CUSTOMERS_CARD_AND_WILL_BE_RELEASED_IN_A_FEW_BUSINESS_DAYS_PLEASE_ENSURE_THE_BILLING_ADDRESS_IS_ACCURATE_BEFORE_RETRYING_THE_TRANSACTION = ResultCode(  # noqa: E501
        code="800.400.110",
        name="AVS_CHECK_FAILED_AMOUNT_HAS_STILL_BEEN_RESERVED_ON_THE_CUSTOMERS_CARD_AND_WILL_BE_RELEASED_IN_A_FEW_"
        "BUSINESS_DAYS_PLEASE_ENSURE_THE_BILLING_ADDRESS_IS_ACCURATE_BEFORE_RETRYING_THE_TRANSACTION",
        description="AVS Check Failed. Amount has still been reserved on the customer's card and will be released in "
        "a few business days. Please ensure the billing address "
        "is accurate before retrying the transaction.",
    )
    IMPLAUSIBLE_ADDRESS_DATA = ResultCode(
        code="800.400.150", name="IMPLAUSIBLE_ADDRESS_DATA", description="Implausible address data"
    )
    IMPLAUSIBLE_ADDRESS_STATE_DATA = ResultCode(
        code="800.400.151", name="IMPLAUSIBLE_ADDRESS_STATE_DATA", description="Implausible address state data"
    )
    INVALID_PAYER_AUTHENTICATION_IN_3DSECURE_TRANSACTION = ResultCode(
        code="800.400.200",
        name="INVALID_PAYER_AUTHENTICATION_IN_3DSECURE_TRANSACTION",
        description="Invalid Payer Authentication in 3DSecure transaction",
    )
    WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_PAYMENT_DENIED_FOR_NOW = ResultCode(
        code="800.400.500",
        name="WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_PAYMENT_DENIED_FOR_NOW",
        description="Waiting for confirmation of non-instant payment. Denied for now.",
    )
    WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_DEBIT_DENIED_FOR_NOW = ResultCode(
        code="800.400.501",
        name="WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_DEBIT_DENIED_FOR_NOW",
        description="Waiting for confirmation of non-instant debit. Denied for now.",
    )
    WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_REFUND_DENIED_FOR_NOW = ResultCode(
        code="800.400.502",
        name="WAITING_FOR_CONFIRMATION_OF_NON_INSTANT_REFUND_DENIED_FOR_NOW",
        description="Waiting for confirmation of non-instant refund. Denied for now.",
    )
    DIRECT_DEBIT_TRANSACTION_DECLINED_FOR_UNKNOWN_REASON = ResultCode(
        code="800.500.100",
        name="DIRECT_DEBIT_TRANSACTION_DECLINED_FOR_UNKNOWN_REASON",
        description="direct debit transaction declined for unknown reason",
    )
    UNABLE_TO_PROCESS_TRANSACTION__RAN_OUT_OF_TERMINALIDS__PLEASE_CONTACT_ACQUIRER = ResultCode(
        code="800.500.110",
        name="UNABLE_TO_PROCESS_TRANSACTION__RAN_OUT_OF_TERMINALIDS__PLEASE_CONTACT_ACQUIRER",
        description="Unable to process transaction - ran out of terminalIds - please contact acquirer",
    )
    TRANSACTION_IS_BEING_ALREADY_PROCESSED = ResultCode(
        code="800.600.100",
        name="TRANSACTION_IS_BEING_ALREADY_PROCESSED",
        description="transaction is being already processed",
    )
    TRANSACTION_FOR_THE_SAME_SESSION_IS_CURRENTLY_BEING_PROCESSED_PLEASE_TRY_AGAIN_LATER = ResultCode(
        code="800.700.100",
        name="TRANSACTION_FOR_THE_SAME_SESSION_IS_CURRENTLY_BEING_PROCESSED_PLEASE_TRY_AGAIN_LATER",
        description="transaction for the same session is currently being processed, please try again later.",
    )
    FAMILY_NAME_TOO_LONG = ResultCode(
        code="800.700.101", name="FAMILY_NAME_TOO_LONG", description="family name too long"
    )
    GIVEN_NAME_TOO_LONG = ResultCode(code="800.700.201", name="GIVEN_NAME_TOO_LONG", description="given name too long")
    COMPANY_NAME_TOO_LONG_2 = ResultCode(
        code="800.700.500", name="COMPANY_NAME_TOO_LONG_2", description="company name too long"
    )
    INVALID_STREET = ResultCode(code="800.800.102", name="INVALID_STREET", description="Invalid street")
    INVALID_ZIP_2 = ResultCode(code="800.800.202", name="INVALID_ZIP_2", description="Invalid zip")
    INVALID_CITY_2 = ResultCode(code="800.800.302", name="INVALID_CITY_2", description="Invalid city")
    CONNECTOR_ACQUIRER_SYSTEM_IS_UNDER_MAINTENANCE = ResultCode(
        code="800.800.400",
        name="CONNECTOR_ACQUIRER_SYSTEM_IS_UNDER_MAINTENANCE",
        description="Connector/acquirer system is under maintenance",
    )
    THE_PAYMENT_SYSTEM_IS_CURRENTY_UNAVAILABLE_PLEASE_CONTACT_SUPPORT_IN_CASE_THIS_HAPPENS_AGAIN = ResultCode(
        code="800.800.800",
        name="THE_PAYMENT_SYSTEM_IS_CURRENTY_UNAVAILABLE_PLEASE_CONTACT_SUPPORT_IN_CASE_THIS_HAPPENS_AGAIN",
        description="The payment system is currenty unavailable, please contact support in case this happens again.",
    )
    THE_PAYMENT_SYSTEM_IS_CURRENTY_UNTER_MAINTENANCE_PLEASE_APOLOGIZE_FOR_THE_INCONVENIENCE_THIS_MAY_CAUSE_IF_YOU_WERE_NOT_INFORMED_OF_THIS_MAINTENANCE_WINDOW_IN_ADVANCE_CONTACT_YOUR_SALES_REPRESENTATIVE = ResultCode(  # noqa: E501
        code="800.800.801",
        name="THE_PAYMENT_SYSTEM_IS_CURRENTY_UNTER_MAINTENANCE_PLEASE_APOLOGIZE_FOR_THE_INCONVENIENCE_THIS_MAY_CAUSE_"
        "IF_YOU_WERE_NOT_INFORMED_OF_THIS_MAINTENANCE_WINDOW_IN_ADVANCE_CONTACT_YOUR_SALES_REPRESENTATIVE",
        description="The payment system is currenty unter maintenance. Please apologize for the inconvenience this may "
        "cause. If you were not informed of this maintenance window in advance, "
        "contact your sales representative.",
    )
    SENDER_AUTHORIZATION_FAILED_ = ResultCode(
        code="800.900.100", name="SENDER_AUTHORIZATION_FAILED_", description="sender authorization failed "
    )
    INVALID_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX_2 = ResultCode(
        code="800.900.101",
        name="INVALID_EMAIL_ADDRESS_PROBABLY_INVALID_SYNTAX_2",
        description="invalid email address (probably invalid syntax)",
    )
    INVALID_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG_2 = ResultCode(
        code="800.900.200",
        name="INVALID_PHONE_NUMBER_HAS_TO_START_WITH_A_DIGIT_OR_A_PLUS_AT_LEAST_7_AND_MAX_25_CHARS_LONG_2",
        description="invalid phone number (has to start with a digit or a '+', at least 7 and max 25 chars long)",
    )
    UNKNOWN_CHANNEL = ResultCode(code="800.900.201", name="UNKNOWN_CHANNEL", description="unknown channel")
    INVALID_AUTHENTICATION_INFORMATION = ResultCode(
        code="800.900.300", name="INVALID_AUTHENTICATION_INFORMATION", description="invalid authentication information"
    )
    USER_AUTHORIZATION_FAILED_USER_HAS_NO_SUFFICIENT_RIGHTS_TO_PROCESS_TRANSACTION = ResultCode(
        code="800.900.301",
        name="USER_AUTHORIZATION_FAILED_USER_HAS_NO_SUFFICIENT_RIGHTS_TO_PROCESS_TRANSACTION",
        description="user authorization failed, user has no sufficient rights to process transaction",
    )
    AUTHORIZATION_FAILED = ResultCode(
        code="800.900.302", name="AUTHORIZATION_FAILED", description="Authorization failed"
    )
    NO_TOKEN_CREATED = ResultCode(code="800.900.303", name="NO_TOKEN_CREATED", description="No token created")
    SECURE_REGISTRATION_PROBLEM = ResultCode(
        code="800.900.399", name="SECURE_REGISTRATION_PROBLEM", description="Secure Registration Problem"
    )
    INVALID_IP_NUMBER_3 = ResultCode(code="800.900.401", name="INVALID_IP_NUMBER_3", description="Invalid IP number")
    INVALID_BIRTHDATE_2 = ResultCode(code="800.900.450", name="INVALID_BIRTHDATE_2", description="Invalid birthdate")
    UNEXPECTED_COMMUNICATION_ERROR_WITH_CONNECTOR_ACQUIRER = ResultCode(
        code="900.100.100",
        name="UNEXPECTED_COMMUNICATION_ERROR_WITH_CONNECTOR_ACQUIRER",
        description="unexpected communication error with connector/acquirer",
    )
    ERROR_RESPONSE_FROM_CONNECTOR_ACQUIRER = ResultCode(
        code="900.100.200",
        name="ERROR_RESPONSE_FROM_CONNECTOR_ACQUIRER",
        description="error response from connector/acquirer",
    )
    ERROR_ON_THE_EXTERNAL_GATEWAY_EG_ON_THE_PART_OF_THE_BANK_ACQUIRER = ResultCode(
        code="900.100.201",
        name="ERROR_ON_THE_EXTERNAL_GATEWAY_EG_ON_THE_PART_OF_THE_BANK_ACQUIRER",
        description="error on the external gateway (e.g. on the part of the bank, acquirer,...)",
    )
    INVALID_TRANSACTION_FLOW_THE_REQUESTED_FUNCTION_IS_NOT_APPLICABLE_FOR_THE_REFERENCED_TRANSACTION = ResultCode(
        code="900.100.202",
        name="INVALID_TRANSACTION_FLOW_THE_REQUESTED_FUNCTION_IS_NOT_APPLICABLE_FOR_THE_REFERENCED_TRANSACTION",
        description="invalid transaction flow, the requested function is not "
        "applicable for the referenced transaction.",
    )
    ERROR_ON_THE_INTERNAL_GATEWAY = ResultCode(
        code="900.100.203", name="ERROR_ON_THE_INTERNAL_GATEWAY", description="error on the internal gateway"
    )
    ERROR_DURING_MESSAGE_PARSING = ResultCode(
        code="900.100.204", name="ERROR_DURING_MESSAGE_PARSING", description="Error during message parsing"
    )
    TIMEOUT_UNCERTAIN_RESULT = ResultCode(
        code="900.100.300", name="TIMEOUT_UNCERTAIN_RESULT", description="timeout, uncertain result"
    )
    TRANSACTION_TIMED_OUT_WITHOUT_RESPONSE_FROM_CONNECTOR_ACQUIRER_IT_WAS_REVERSED = ResultCode(
        code="900.100.301",
        name="TRANSACTION_TIMED_OUT_WITHOUT_RESPONSE_FROM_CONNECTOR_ACQUIRER_IT_WAS_REVERSED",
        description="Transaction timed out without response from connector/acquirer. It was reversed.",
    )
    TRANSACTION_TIMED_OUT_DUE_TO_INTERNAL_SYSTEM_MISCONFIGURATION_REQUEST_TO_ACQUIRER_HAS_NOT_BEEN_SENT = ResultCode(
        code="900.100.310",
        name="TRANSACTION_TIMED_OUT_DUE_TO_INTERNAL_SYSTEM_MISCONFIGURATION_REQUEST_TO_ACQUIRER_HAS_NOT_BEEN_SENT",
        description="Transaction timed out due to internal system misconfiguration. "
        "Request to acquirer has not been sent.",
    )
    TIMEOUT_AT_CONNECTORS_ACQUIRER_SIDE = ResultCode(
        code="900.100.400",
        name="TIMEOUT_AT_CONNECTORS_ACQUIRER_SIDE",
        description="timeout at connectors/acquirer side",
    )
    TIMEOUT_AT_CONNECTORS_ACQUIRER_SIDE_TRY_LATER = ResultCode(
        code="900.100.500",
        name="TIMEOUT_AT_CONNECTORS_ACQUIRER_SIDE_TRY_LATER",
        description="timeout at connectors/acquirer side (try later)",
    )
    CONNECTOR_ACQUIRER_CURRENTLY_DOWN = ResultCode(
        code="900.100.600", name="CONNECTOR_ACQUIRER_CURRENTLY_DOWN", description="connector/acquirer currently down"
    )
    ERROR_ON_THE_EXTERNAL_SERVICE_PROVIDER = ResultCode(
        code="900.100.700",
        name="ERROR_ON_THE_EXTERNAL_SERVICE_PROVIDER",
        description="error on the external service provider",
    )
    MESSAGE_SEQUENCE_NUMBER_OF_CONNECTOR_OUT_OF_SYNC = ResultCode(
        code="900.200.100",
        name="MESSAGE_SEQUENCE_NUMBER_OF_CONNECTOR_OUT_OF_SYNC",
        description="Message Sequence Number of Connector out of sync",
    )
    USER_SESSION_TIMEOUT = ResultCode(
        code="900.300.600", name="USER_SESSION_TIMEOUT", description="user session timeout"
    )
    UNEXPECTED_COMMUNICATION_ERROR_WITH_EXTERNAL_RISK_PROVIDER = ResultCode(
        code="900.400.100",
        name="UNEXPECTED_COMMUNICATION_ERROR_WITH_EXTERNAL_RISK_PROVIDER",
        description="unexpected communication error with external risk provider",
    )
    UNDEFINED_PLATFORM_DATABASE_ERROR = ResultCode(
        code="999.999.888", name="UNDEFINED_PLATFORM_DATABASE_ERROR", description="UNDEFINED PLATFORM DATABASE ERROR"
    )
    UNDEFINED_CONNECTOR_ACQUIRER_ERROR = ResultCode(
        code="999.999.999", name="UNDEFINED_CONNECTOR_ACQUIRER_ERROR", description="UNDEFINED CONNECTOR/ACQUIRER ERROR"
    )

    def __init__(self):
        """Set each provided result code by field."""
        self.by_code = dict()
        for attr in dir(self):
            if isinstance(getattr(self, attr), ResultCode):
                self.by_code[getattr(self, attr).code] = getattr(self, attr)

    def get(self, code: str) -> ResultCode:
        """Get result code.

        Args:
            - code (str): ResultCode number

        Returns:
            the result code identified by code number.

        Raises:
            KeyError if code not instantiated.
        """
        return self.by_code[code]


result_codes = ResultCodes()
