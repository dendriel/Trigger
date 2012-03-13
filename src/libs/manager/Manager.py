# -*-coding:utf-8-*-
import socket
import time
from threading import Thread
from datetime import datetime
from libs.log.slog import slog
from libs.defines.defines import *
from libs.shared.shared import shared
from libs.dbcom.Pgcom import Pgcom

# Macros #
ID   = 0
BLOW = 1
SEND = 2
#--------#

class Manager:

    def __init__(self, log_obj, gsmcom):

        self.log = log_obj
        self.shared = shared()
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
            # do receiveService()
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
            now = now.replace(second=0, microsecond=0)

            # look for requisitions to send #
            for req in active_list:

                sub = req[BLOW] - now
                # change from timedelta to int #
                sub = sub.total_seconds()

                # if it delayed ore than the maximum #
                if sub < MAX_TIME_TO_SEND:
                    if self.dbcom.changeRequisitionStatus(req[ID], FAILED) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[ID])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton status changed to FAILED. Requisiton id=\"%d\"" % req[ID])

                # if is to be sent as soon as possible #
                elif req[SEND] == True:
                    self.log.LOG(content="changing status for %d" % req[ID])
                    self.completeRequisition(req[ID])
                    if self.dbcom.changeRequisitionStatus(req[ID], SENT) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[ID])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton status changed to SENT. Requisiton id=\"%d\"" % req[ID])

                # is not yet to be sent #
                elif sub <= MIN_TIME_TO_SEND:
                    self.log.LOG(content="changing status for %d" % req[ID])
                    self.completeRequisition(req[ID])
                    if self.dbcom.changeRequisitionStatus(req[ID], SENT) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[ID])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton status changed to SENT. Requisiton id=\"%d\"" % req[ID])

                # should not fall here #
                else:
                    if self.dbcom.changeRequisitionStatus(req[ID], FAILED) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[ID])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton status changed to FAILED. Requisiton id=\"%d\"" % req[ID])

            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.sendService()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def completeRequisition(self, req_id):

        data_dict = self.dbcom.getDataFromRequisition(req_id)
        print data_dict
