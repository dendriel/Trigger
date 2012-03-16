# -*-coding:utf-8-*-
import socket
import time
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

            self.sendService()
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
            # !(the sendSMS line is commented because i'm not rich
            # and cant afford more credits to send SMS. =})
            if self.gsmcom.sendSMS(destination, message) != OK:
                ret = ERROR

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

        # recover data from the GSM module #
        for msg_index in range(msg_count):
            msg_index += 1
            msg_data = self.gsmcom.getMessageByIndex(msg_index)

            if msg_data == ERROR:
                self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to register requisition from SIMCARD ID [%d]. Ignoring..." % msg_index)
                self.gsmcom.deleteMessage(msg_index)
                continue

            self.log.LOG(content=msg_data)
            continue # from here to bottom the functions do not exist yet #
            msg_req = self.mountRequisition(msg_data)

            if msg_req != ERROR:
                if self.dbcom.registerRequisition(msg_req) != OK:
                    if self.dbcom.registerRequisition(msg_req) != OK:
                        self.log.LOG(LOG_CRITICAL, "manager.receiveService()", "Failed to register requisition from SIMCARD ID [%d]. Ignoring..." % msg_index)
                    else:
                        self.log.LOG(LOG_INFO, "manager", "Registered new requisition via GSM module.") # TODO show what is the req ID in the db #
                else:
                    self.log.LOG(LOG_INFO, "manager", "Registered new requisition via GSM module.") # TODO show what is the req ID in the db #

            self.gsmcom.deleteMessage(msg_index)

        return
