import time
import socket
from mx.DateTime import now
from libs.defines.defines import *
from libs.shared.shared import *
from libs.log.slog import slog

class alarm:
##
# Brief: Initialing objects to processing.
##
	def __init__(self, log_path):
		self.log = slog(log_path)
		self.shared = shared()
##
# Brief: The alarm function will need do calculation about the time to sleep, and
# when he wake up will need to send data to main system, asking for the alarm to blow.
##
	def launch(self, orig, destination, content, blow, counter):

		try:
			sleep_time = int(blow - now())
			self.log.LOG(LOG_INFO, "alarm", "New alarm has been scheduled. Blow date/time in %s. It's take %d seconds from now." % (blow, sleep_time))

			time.sleep(sleep_time)
			
			channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			channel.connect(("127.0.0.1", SYSTEM_PORT))
			package = "\ID:102/ID\CMD:blow/CMD\CONTENT:%s: %s/CONTENT\HOWMANY:1/HOWMANY\DATA:\PART0:%s/PART0/DATA\FROM:%d/FROM" % (orig, content, destination, counter)
			channel.send(package)

			status = int(channel.recv(MSG_SIZE))
			self.log.LOG(LOG_INFO, "alarm", "Alarm thread finished with status: %s." % RETURN[status])

		except socket.error, msg:
			self.log.LOG(LOG_CRITICAL, "alarm.launch()", "The scheduled alarm failed to contact the system. Error: %s" % msg)
			channel.close()

		except:
			self.log.LOG(LOG_CRITICAL, "alarm.launch()", "The alarm thread has a problem and will be aborted.")	
##
# Brief: Mounts a dictionary with the content of 
#	TAGs in the data package.
# Param: cmsg The data package.
# Return: The data dictionary if all the data is OK;
#	ERROR if something is missing.
##
	def retrieveData(self, cmsg):

		sms_dict = {}
		# Originator #
		ret = self.shared.splitTag(cmsg, TAG_FROM)
		if ret == NOTFOUND:
			return NOTFOUND

		else:
			sms_dict[DATA_ORG] = ret

		ret = self.shared.splitTag(cmsg, TAG_CONTENT)
		# Message #
		if ret == NOTFOUND:
			return NOTFOUND

		else:
			sms_dict[DATA_MSG] = ret

		ret = self.shared.splitTag(cmsg, TAG_BLOW)
		# Blow #
		if ret == NOTFOUND:
			return NOTFOUND
		else:
			sms_dict[DATA_BLOW] = ret

		ret = self.shared.splitTag(cmsg, TAG_HOWMANY)
		# How many destinations #
		if ret == NOTFOUND:
			return NOTFOUND
		else:
			sms_dict[DATA_DESTN] = ret

		for index in range (0, sms_dict[DATA_DESTN]):

			ret = self.shared.splitTag(cmsg, TAG_PART, index)
			if ret == NOTFOUND:
				return NOTFOUND
			else:
				sms_dict[DATA_EXT + "%d" % index] = ret

		# Operator #
		for index in range (0, sms_dict[DATA_DESTN]):

			ret = self.shared.splitTag(cmsg, TAG_INFO, index)
			if ret ==  NOTFOUND:
				return NOTFOUND
			else:
				sms_dict[DATA_OPER + "%d" % index] = int(ret)

		return sms_dict

