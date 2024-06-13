from enum import Enum

SDK_LIBRARY = "fga-python"
SDK_VERSION = "0.1.0"

EU_ZONE = "EU"
DEFAULT_ZONE = "US"
BATCH = 'batch'
HTTP_V2 = 'v2'
EVENT = 'event'
USER = 'user'
ACCOUNT = 'account'
ASSET = 'asset'
SESSION = 'session'
SERVER_URL = {
    EVENT: 'https://www.footprint.network/api/v1/fga/sdk/event',
    USER: 'https://www.footprint.network/api/v1/fga/sdk/user',
    ACCOUNT: 'https://www.footprint.network/api/v1/fga/sdk/account',
    ASSET: 'https://www.footprint.network/api/v1/fga/sdk/asset',
    SESSION: 'https://www.footprint.network/api/v1/fga/sdk/session'
}
LOGGER_NAME = "amplitude"

IDENTIFY_EVENT = "$identify"
GROUP_IDENTIFY_EVENT = "$groupidentify"
IDENTITY_OP_ADD = "$add"
IDENTITY_OP_APPEND = "$append"
IDENTITY_OP_CLEAR_ALL = "$clearAll"
IDENTITY_OP_PREPEND = "$prepend"
IDENTITY_OP_SET = "$set"
IDENTITY_OP_SET_ONCE = "$setOnce"
IDENTITY_OP_UNSET = "$unset"
IDENTITY_OP_PRE_INSERT = "$preInsert"
IDENTITY_OP_POST_INSERT = "$postInsert"
IDENTITY_OP_REMOVE = "$remove"
UNSET_VALUE = "-"

REVENUE_PRODUCT_ID = "$productId"
REVENUE_QUANTITY = "$quantity"
REVENUE_PRICE = "$price"
REVENUE_TYPE = "$revenueType"
REVENUE_RECEIPT = "$receipt"
REVENUE_RECEIPT_SIG = "$receiptSig"
REVENUE = "$revenue"
AMP_REVENUE_EVENT = "revenue_amount"

MAX_PROPERTY_KEYS = 1024
MAX_STRING_LENGTH = 1024
FLUSH_QUEUE_SIZE = 200
FLUSH_INTERVAL_MILLIS = 10000
FLUSH_MAX_RETRIES = 12
CONNECTION_TIMEOUT = 10.0  # seconds float
MAX_BUFFER_CAPACITY = 20000


DEFAULT_HEADER = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*", "User-Agent": "Mozilla/5.0"
}


class PluginType(Enum):
    BEFORE = 0
    ENRICHMENT = 1
    DESTINATION = 2
    OBSERVE = 3


class UserPropertiesOperation(Enum):
    SET = 'set'
    SET_ONCE = 'set_once'
