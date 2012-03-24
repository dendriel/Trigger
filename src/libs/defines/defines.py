# RETURN VALUES #
OK       =  0
ERROR    = -1
INVALID  = -2
NOTFOUND = -4

# RETURN VALUES STRINGS #
RETURN = {OK:"OK", ERROR:"ERROR", INVALID:"INVALID", NOTFOUND:"NOTFOUND"}

# TAGS #
TAG_ID      = "ID"
TAG_CMD     = "CMD"
TAG_INFO    = "INFO"
TAG_DATA    = "DATA"
TAG_FROM    = "FROM"
TAG_CONTENT = "CONTENT"
TAG_HOWMANY = "HOWMANY"
TAG_BLOW    = "BLOW"
TAG_PART    = "PART"

# REQUISITION DATA #
DATA_ORIG   = "orig"    # A name to identify the origin.                                 #
DATA_DESTN  = "dest"    # The destination numbers.                                       #
DATA_MSG    = "msg"     # The message to be sent.                                        #
DATA_OPER   = "oper"    # An operator indicator. *See operator definitions* *not in use* #
DATA_SEND   = "send"    # A flag that informs if the requisition is to be executed now.  #
DATA_BLOW   = "blow"    # The date/time when the requisition will be sent.               #
DATA_STATUS = "stat"    # The state of the requisition. *See requisition states*         #
DATA_ID     = "id"      # The unique identifier of the requisition.                      #
DATA_DATE   = "date"    # When the requisition was sent to the system. *not in use*      #

# REQUISITION STATES #
ACTIVE   = 0
CANCELED = 1
FAILED   = 2
SENT     = 3

# OPERATOR DEFINITIONS #
VIVO  = 0
OI    = 1
TIM   = 2
CLARO = 3

# LOG LEVELS #
LOG_INFO     = 10
LOG_ERROR    = 11
LOG_CRITICAL = 12

# MISC #
MAX_CONNECTIONS = 5
MSG_SIZE = 4096

# FILE NAMES #
SMS_LOGNAME   = "sms.log"
DBCOM_LOGNAME = "dbcom.log"
ALARM_LOGNAME = "alarm.log"

# DATABASE DEFINITIONS #
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "trigger"
DB_PASS = "trigger"
DB_NAME = "trigger"

TABLE_SMS  = "sms"
DB_TABLES = (TABLE_SMS,)

# LIST OF COMMANDS #
CMD_HALT     = "halt"
CMD_CLEAN_LOG     = "clean_log"
CMD_SEND_SMS     = "send_sms"
CMD_LOGIN     = "login"
CMD_BLOW     = "blow"


# GSM COMMUNICATION #
GSM_ATCOM     = 20
GSM_ASTERISK     = 21

# SYSTEM DEFINITIONS #
SYSTEM_PORT = 3435
SYSTEM_LOG_PATH = "./system.out"

# ETC #
MNGR_THRD_SLEEP = 10 # seconds
EMPTY = ""
NULL_LIST = []
MIN_TIME_TO_SEND = 10 # The minimum "at least" time to send #
MAX_TIME_TO_SEND = -60 # The maximum time before the blow to send #
SEPARATOR_CHAR = '@'
SEPARATOR_CHAR_FOR_DB = ','
MAX_ORIG_LEN = 7       # Maximum string length to identify the origin            #
MAX_DEST_CODE_LEN = 7   # Maximum string length to identify the destination group #
MODULE_PORT = "/dev/ttyACM0"
RPC_PATHS = ('/RPC2')

# Validator Parameters #
VALIDATOR_PATH    = "../daemon_modules/validator.php" # not really defined yet... #
GET_NUMBER_PATH   = "../daemon_modules/get_contacts.php" # not really defined yet... #
VAL_NUMB_EXIST    = 0     # The validated number exist in database and is from a teacher #
VAL_NUMB_MISSING  = 1     # The validated number does not exist for a teacher            #
VAL_PROC_ERROR    = 2     # The validator failed to process the number                   #
INTERPRETER       = "php" # what interpreter will run the "modular scripts" #


# AT RETURN VALUES #
AT_OK = "0"
AT_ERROR = "4"
AT_ERROR_ST = "ERROR" # at error string #
