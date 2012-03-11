# -*-coding:utf-8-*-
import socket
import time
from threading import Thread
from datetime import datetime
from libs.log.slog import slog
from libs.defines.defines import *
from libs.shared.shared import shared
from libs.dbcom.Pgcom import Pgcom


class Manager:

    def __init__(self, log_obj, ):

        self.log = log_obj
        self.shared = shared()
        self.monitor_thread = ''
        self.dbcom = Pgcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT, self.log)

    def launchMonitor(self):

        try:
            self.monitor_thread = Thread(target=self.smsEvents)
            self.monitor_thread.start()
            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.launchMonitor()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def smsEvents(self):

        while(True):

            self.sendService()
            # do receiveService()
            time.sleep(MNGR_THRD_SLEEP)

    def sendService(self):

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
                sub = req[1] - now
                # change from timedelta to int #
                sub = sub.total_seconds()

                if sub < MAX_TIME_TO_SEND:

                    if self.dbcom.changeRequisitionStatus(req[0], FAILED) == ERROR:
                        self.log.LOG(LOG_CRITICAL, "manager.sendService()", "Failed to change requisition status. Requisiton id=\"%d\"" % req[0])
                    else:
                        self.log.LOG(LOG_INFO, "manager.sendService()", "Requisiton status changed to FAILED. Requisiton id=\"%d\"" % req[0])

                elif sub <= MIN_TIME_TO_SEND:
                    self.log.LOG(content="changing status for %d" % req[0])
                    self.completeRequisition(req[0])
                    self.dbcom.changeRequisitionStatus(req[0], SENT)

            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.sendService()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def completeRequisition(self, req_id):

        data_dict = self.dbcom.getDataFromRequisition(req_id)
        print data_dict
