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

# REQUISITION DATA #
DATA_ORIG   = "orig"    # A name to identify the origin.                                 #
DATA_DESTN  = "dest"    # The destination numbers.                                       #
DATA_MSG    = "msg"     # The message to be sent.                                        #
DATA_OPER   = "oper"    # An operator indicator. *not in use in this implementation*     #
DATA_SEND   = "send"    # A flag that informs if the requisition is to be executed now.  #
DATA_BLOW   = "blow"    # The date/time when the requisition will be sent.               #
DATA_STATUS = "stat"    # The state of the requisition. *See requisition states*         #
DATA_ID     = "id"      # The unique identifier of the requisition.                      #

# REQUISITION STATES #
ACTIVE   = 0
CANCELED = 1
FAILED   = 2
SENT     = 3

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
