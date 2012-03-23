# -*-coding:utf-8-*-
import time
import subprocess
from threading import Thread
from datetime import datetime
from libs.defines.defines import *
from libs.dbcom.Pgcom import Pgcom

# Macros #
ID   = 0
BLOW = 1
SEND = 2
#--------#

class Manager:

    def __init__(self, log_obj, gsmcom):
        """
        Param: log_obj A slog object to use to log infos.
        Param: gsmcom A gsmcommunication to use SMS service.
        """
        self.log = log_obj
        self.monitor_thread = ''
        self.dbcom = Pgcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT, self.log)
        self.gsmcom = gsmcom

    def launchMonitor(self):
        """
        Brief: Set manager thread and launch it.
        Return: OK if could launch the thread; ERROR otherwise.
        """
        try:
            self.monitor_thread = Thread(target=self.smsEvents)
            self.monitor_thread.start()
            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.launchMonitor()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def smsEvents(self):
        """
        Brief: Main loop for manager Thread.
        """
        while(True):

            #self.log.LOG(LOG_INFO, "manager", "Executing sendService()...")
            self.sendService()
            #self.log.LOG(LOG_INFO, "manager", "Executing receiveService()...")
            self.receiveService()
            time.sleep(MNGR_THRD_SLEEP)

    def sendService(self):
        """
        Brief: Retrieve a list of active requisitions from the database, 
            test it, do some action and if is necessary update the 
            requisition status.
        Return: OK if everything went fine; ERROR otherwise.
        """
        try:
            # recover active requisitions #
            active_list = self.dbcom.getRequisitions(ACTIVE)

            if active_list == NULL_LIST:
                return OK
            else:
                active_list == active_list[0]

            now = datetime.now()
            now = now.replace(microsecond=0)

            # look for requisitions to send #
            for req in active_list:

                sub = req[BLOW] - now
                # change from timedelta to int #
                sub = sub.total_seconds()

                # if it delayed more than the maximum #
                if sub < MAX_TIME_TO_SEND:
                    if self.dbcom.changeRequisitionStatus(req[ID], FAILED) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[ID])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton FAILED due to timeout to blow (%ds). Requisiton id=\"%d\"" % (sub, req[ID]))

                # if is to be sent as soon as possible #
                elif req[SEND] == True:
                    self.completeRequisition(req[ID])

                # is yet to be sent #
                elif sub <= MIN_TIME_TO_SEND:
                    self.completeRequisition(req[ID])

            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.sendService()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def completeRequisition(self, req_id):

        ret = OK
        data_dict = self.dbcom.getDataFromRequisition(req_id)
        message = ""
        message += data_dict[DATA_ORIG]
        message += ": " 
        message += data_dict[DATA_MSG]

        for destination in data_dict[DATA_DESTN]:
            ret = OK 

            if self.gsmcom.sendSMS(destination, message) != OK:
                ret = ERROR

            self.log.LOG(LOG_INFO, "manager", "SMS sent to destination: %s" % destination)
                

        if ret == OK:
            req_state = SENT
        else:
            req_state = FAILED

        if self.dbcom.changeRequisitionStatus(req_id, req_state) == ERROR:
            self.log.LOG(LOG_CRITICAL, "manager.compĺeteRequisition()", "Failed to change requisition status. Requisiton id=\"%d\"" % req_id)
        else:
            self.log.LOG(LOG_INFO, "manager.completeRequisition()", "Requisiton status changed to SENT. Requisiton id=\"%d\"" % req_id)

        return

    def receiveService(self):
        """
        Brief: Question to the GSM module for new messages and process if there are any.
        Return: None.
        """
        msg_count = self.gsmcom.getMessagesCount()
        if msg_count == ERROR:
            self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to retrieve messages count. Can not go forward.")
            return

        # recover data from the GSM module #
        for msg_index in range(msg_count):
            msg_index += 1
            msg_data = self.gsmcom.getMessageByIndex(msg_index)

            if msg_data == ERROR:
                self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to register requisition from module, message ID [%d]. Ignoring..." % msg_index)
                self.gsmcom.deleteMessage(msg_index)
                continue

            msg_req = self.mountRequisition(msg_data)

            if msg_req == ERROR:
                self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to mount requisition. Message ID [%d]. Ignoring..." % msg_index)
                self.gsmcom.deleteMessage(msg_index)
                continue

            elif msg_req == INVALID:
                self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Invalid requisition received. Message ID [%d]. Ignoring..." % msg_index)
                self.gsmcom.deleteMessage(msg_index)
                continue

            else:
                if self.dbcom.registerRequisition(msg_req) != OK:
                    if self.dbcom.registerRequisition(msg_req) != OK:
                        self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to register requisition from SIMCARD ID [%d]. Ignoring..." % msg_index)
                    else:
                        self.log.LOG(LOG_INFO, "manager", "Registered new requisition via GSM module.") # TODO show what is the req ID in the db #
                else:
                    self.log.LOG(LOG_INFO, "manager", "Registered new requisition via GSM module.") # TODO show what is the req ID in the db #

            self.gsmcom.deleteMessage(msg_index)

        return

    def mountRequisition(self, msg_data):
        """
        Brief: Validate and mount a service requisition.
        Param: msg_data The data package.
        Return: A dict with the data requisition if it is valid;
                INVALID if the requisition could not be understood.
                ERROR otherwise.
        """
        # Create the script to validate origin and retrieve destination list #
        #ret = self.validateOrigin(msg_data[DATA_ORIG])
        ret = OK # Remove this line and uncomment line above; its for testing purpose #
        if ret == INVALID:
            return INVALID

        elif ret == ERROR:
            self.log.LOG(LOG_ERROR, "manager.mountRequisition()", "An error ocurred while validating requisition from gsm module.")
            return ERROR

        msg_values = self.getValuesFromMessage(msg_data[DATA_MSG])

        if msg_values == ERROR:
            self.log.LOG(LOG_ERROR, "manager.mountRequisition()", "An error ocurred processing data from gsm module.")
            return ERROR

        # dest_list -> needs to retrieve specified group cellphone address
        dest_list = "91553900,91553900,91553900"

        try:
            req_dict = {
                        DATA_MSG: msg_values[DATA_MSG],\
                        DATA_ORIG:msg_values[DATA_ORIG],\
                        DATA_SEND:msg_values[DATA_SEND],\
                        DATA_BLOW:msg_values[DATA_BLOW],\
                        DATA_DESTN:dest_list,\
                        DATA_OPER:VIVO\
                        }
        except Exception, exc:
            self.log.LOG(LOG_ERROR, "manager.mountRequisition()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

        return req_dict

    def getValuesFromMessage(self, message_body):
        """
        Brief: Retrieve the values from the message if he is consistent.
        Param: msg_data The body text from the message.
        Return: A dict with data from the requisition;
                ERROR if something went wrong.
        """
        MIN_DATA_VALUES = 3 # minimum fields needed in the message body #
        # content position #
        ORIG_P = 0
        CODE_P = 1
        DATETIME_P = 2
        MSG_P = 3
        try:
            values = message_body.split(SEPARATOR_CHAR)
            len_values = len(values)

            if len_values >= MIN_DATA_VALUES:
            	orig = values[ORIG_P][0:MAX_ORIG_LEN]
            	dest_code = values[CODE_P][0:MAX_DEST_CODE_LEN]
                dt_data = values[DATETIME_P]

                date_time = self.retrieveDateTime(dt_data)
                # if date/time formt is invalid #
                if date_time == ERROR:
                    return ERROR

                msg = ""
                for index in range(MSG_P, len_values):
                    msg+= values[MSG_P]
                    if index < len_values:
                        msg+= " " # put spaces between text words #
                
                return {DATA_ORIG:orig, DATA_MSG:msg, DATA_SEND:date_time[DATA_SEND], DATA_BLOW:str(date_time[DATA_BLOW])}

            else:
                self.log.LOG(LOG_ERROR, "manager.getValuesFromMessage()", "Message body is not correctly formated. Values Length: %d" % len(values))
                return ERROR
                    
                    
            # TODO try to recover a date/time value; if was not possible, add the field to the message
            
        except Exception, exc:
            self.log.LOG(LOG_ERROR, "manager.getValuesFromMessage()", "Error while mounting dictionary. %s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def validateOrigin(self, number):
        """
        Brief: Call a extern script that will validate the given number.
        Param: number The number to validate.
        Return: OK if the number is trusted; INVALID if the number does not
                exist; ERROR if something went wrong
        """
        try:
            valitation_val = subprocess.Popen([VALIDATOR_PATH, number]);

            if validation_val == VAL_NUM_EXIST:
                return OK
    
            elif validation_val == VAL_NUM_MISSING:
                return INVALID
    
            else:
                return ERROR

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "manager.validateOrigin()", "Error while validating origin from requisition. %s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def retrieveDateTime(self, dt_data):
        """
        Brief: Try to retrieve date/time value from the data package.
        Param: data The package to be checked.
        Return: A timestamp corresponding to the date/time recovered
                from the package; ERROR if the date/time forma is not
                valid;
        """
        DAY_MAX = 31 # TODO validate february months and leap years
        MONTH_MAX = 12
    
        try:
            dt_len = len(dt_data)
        
            if dt_len == 0:
                    return {DATA_SEND:True, DATA_BLOW:datetime.now()}
          
            elif dt_len == 5: # expect hour:min ~ ex.: 16:40 #
        
                time = self.verifyTime(dt_data)
            
                if time != ERROR:
                    now = datetime.now()
                    now = now.replace(hour=time[0], minute=time[1], microsecond=0)
                    return {DATA_SEND:False, DATA_BLOW:now}
        
                else:
                    return ERROR
        
            elif dt_len == 11:
                dt_data = dt_data.split()
                date = dt_data[0] 
                time = dt_data[1]
        
                if date.find("/") == ERROR:
                    return ERROR
        
                else:
                    date = date.split("/")
                    date[0] = int(date[0])
                    date[1] = int(date[1])
        
                    if date[0] > DAY_MAX or date[0] <= 0:
                        return ERROR
        
                    elif date[1] > MONTH_MAX or date[0] <= 0:
                        return ERROR
        
                time = self.verifyTime(time)
        
                if time != ERROR:
                    now = datetime.now()
                    now = now.replace(day=date[0], month=date[1], hour=time[0], minute=time[1], microsecond=0)
                    return {DATA_SEND:False, DATA_BLOW:now}
        
                else:
                    return ERROR
        
            else:
                return ERROR

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "manager.retrieveDateTime()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR
    
    def verifyTime(self, dt_data):
        """
        Brief:
        Param: dt_data
        Return:
        """
        HOUR_MAX = 23
        MIN_MAX = 59
    
        try:
            if dt_data.find(":") == ERROR:
                return ERROR
        
            else:
                time = dt_data.split(":")
                time[0] = int(time[0])
                time[1] = int(time[1])
        
                if time[0] > HOUR_MAX:
                    return ERROR
        
                elif time[1] > MIN_MAX:
                    return ERROR
        
                else:
                    return time

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "manager.verifyTime()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

