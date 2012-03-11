# RETURN VALUES #
OK       =  0
ERROR    = -1
INVALID  = -2
NOTFOUND = -4

# RETURN VALUES STRINGS #
RETURN = {OK:"OK", ERROR:"ERROR", INVALID:"INVALID", NOTFOUND:"NOTFOUND"}

# TAGS #
TAG_ID = 	"ID"
TAG_CMD = 	"CMD"
TAG_INFO = 	"INFO"
TAG_DATA = 	"DATA"
TAG_FROM = 	"FROM"
TAG_CONTENT = 	"CONTENT"
TAG_HOWMANY = 	"HOWMANY"
TAG_BLOW = 	"BLOW"
TAG_PART = 	"PART"

# DATA #
DATA_ORIG 	= "orig"
DATA_MSG 	= "msg"
DATA_BLOW 	= "blow"
DATA_OPER 	= "oper"
DATA_DESTN 	= "dest"
DATA_EXT 	= "extension"
DATA_ID = "id"
DATA_STATUS = "stat"

# LOG LEVELS #
LOG_INFO     = 10
LOG_ERROR    = 11
LOG_CRITICAL = 12

# MISC #
MAX_CONNECTIONS = 5
MSG_SIZE = 4096


# FILE NAMES #
SMS_LOGNAME = 	"sms.log"
DBCOM_LOGNAME = "dbcom.log"
ALARM_LOGNAME = "alarm.log"

# DATABASE DEFINITIONS #
DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "trigger"
DB_PASS = "trigger"
DB_NAME = "trigger"

TABLE_SMS  = "sms"
DB_TABLES = (TABLE_SMS,)

# LIST OF COMMANDS #
CMD_HALT 	= "halt"
CMD_CLEAN_LOG 	= "clean_log"
CMD_SEND_SMS 	= "send_sms"
CMD_LOGIN 	= "login"
CMD_BLOW 	= "blow"

# LIST OF ALARMS STATE #
ACTIVE   = 0
CANCELED = 1
FAILED   = 2
SENT     = 3

# GSM COMMUNICATION #
GSM_ATCOM 	= 20
GSM_ASTERISK 	= 21

# SYSTEM DEFINITIONS #
SYSTEM_PORT = 3435
SYSTEM_LOG_PATH = "./system.out"

# ETC #
MNGR_THRD_SLEEP = 10 # seconds
EMPTY = ""
NULL_LIST = []
MIN_TIME_TO_SEND = 10 # The minimum "at least" time to send #
MAX_TIME_TO_SEND = -60 # The maximum time before the blow to send #
SEPARATOR_CHAR = ','
