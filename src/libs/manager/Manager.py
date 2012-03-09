# -*-coding:utf-8-*-
import socket
from threading import Thread
from mx.DateTime import now
from libs.log.slog import slog
from libs.defines.defines import *
from libs.alarm.alarm import alarm
from libs.shared.shared import shared

class Manager:

    def __init__(self, log_obj):

        self.log = log_obj
        self.shared = shared()
        self.monitor_thread = ''

    def launchMonitor(self):

        try:
            self.monitor_thread = Thread(target=self.smsEvents())
            self.monitor_thread.start()

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "manager.launchMonitor()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def smsEvents(self):

        while(True):
            self.log.LOG(LOG_CRITICAL, "manager.smsEvents()", "THREAD RODANDO!!!")

            # do sendService()
            # do receiveService()
            # sleep()






##
# Brief: Schedule an alarm.
##
    def actionScheduleAlarm(self, cmsg, dbcom):

        sms_dict = self.alarm.retrieveData(cmsg)

        activity = ACTIVE

        if sms_dict == NOTFOUND:
            self.log.LOG(LOG_ERROR, "manager", "TAGs are missing in the requisition to schedule an alarm. Aborting schedule.")
            return NOTFOUND

        blow = self.shared.mountTime(sms_dict[DATA_BLOW])

        if blow == INVALID:
            return INVALID

        elif blow < now() or blow == now():
            activity = FAILED

        for i in range(0, sms_dict[DATA_DESTN]):

            ret = dbcom.registerAlarm(sms_dict[DATA_ORG], sms_dict[DATA_EXT+"%d" % i], sms_dict[DATA_BLOW], sms_dict[DATA_OPER+"%d" % i], sms_dict[DATA_MSG], activity)

            if ret == OK and activity == ACTIVE:
                alarm_counter = dbcom.getHigherCounter()
                alarm_thread = Thread(target=self.alarm.launch, args=(sms_dict[DATA_ORG], sms_dict[DATA_EXT+"%d" % i], sms_dict[DATA_MSG], blow, alarm_counter,))
                alarm_thread.start()
                self.log.LOG(LOG_INFO, "sms", "New alarm thread has been started. Counter: %ld" % alarm_counter)

        if ret == OK and activity == ACTIVE:
            return OK

        if ret == NOTFOUND:
            return NOTFOUND

        elif activity == FAILED:
            return INVALID

        else:
            return ERROR

