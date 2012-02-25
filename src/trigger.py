#! /usr/bin/python
# -*-coding:utf-8-*-
import socket
import sys
from time import *
from threading import Thread
from libs.log.slog import slog
from libs.defines.defines import *
from libs.alarm.alarm import alarm
from libs.shared.shared import shared
from libs.dbcom.dbcom import dbcom
from libs.gsmcom.Atcom import Atcom
from interfaces.Manager import Manager
from interfaces.Web import Web

class sms:

##
# Brief: Just initializes the system. Bind socket and stuff :>
# Param: addres The IP to listen for connections
# Param: port The port to listen for connections
# Param: log The path to the log file
##
	def __init__(self, address, port, log, gsm_com_type):

		self.address = address
		self.port = port
		self.channel = '' 
		self.alarm_list = [] 
		self.gsmcom = ''
		self.log_path_list = {SMS_LOGNAME:"%s/%s" % (log, SMS_LOGNAME), ALARM_LOGNAME:"%s/%s" % (log, ALARM_LOGNAME), DBCOM_LOGNAME:"%s/%s" % (log, DBCOM_LOGNAME)}

		try:
			self.log = slog(self.log_path_list[SMS_LOGNAME])
			self.shared = shared()
			self.dbcom = dbcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, self.log_path_list[DBCOM_LOGNAME])
			self.manager = Manager(self.log_path_list[SMS_LOGNAME], self.log_path_list[ALARM_LOGNAME])
			self.web = Web(self.log_path_list[SMS_LOGNAME], self.dbcom)
			if gsm_com_type == GSM_ATCOM:
				self.gsmcom = Atcom(logname=self.log_path_list[SMS_LOGNAME], atLogPath=log)

			elif gsm_com_type == GSM_ASTERISK:
				raise Exception

			else:
				raise Exception

		except:
			print "Failed to create one of the objects."
			sys.exit(0)
##
# Brief: Call all necessary functions and goes into the connection loop
##
	def start(self):

		self.log.LOG(LOG_INFO, "sms", "Starting the system.")
		self.checkConnection()
		self.log.LOG(LOG_INFO, "sms", "System started.")

		self.dbcom.getHigherCounter()

		self.lookForConnection()
		self.channel.close
		sys.exit(0)
##
# Brief: Set the system connection and bind to
# Return: OK if everything went fine; Or halt the system if unsucess
##		
	def checkConnection (self):

		try:
			self.channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.channel.bind((self.address, self.port))
			self.channel.listen(MAX_CONNECTIONS)
			self.log.LOG(LOG_INFO, "sms", "System listening channel is OK.") 

		except socket.error, msg:
			self.channel.close()
			self.log.LOG(LOG_CRITICAL, "sms.checkConnection()", "Failed to set the server listening connection. Error: %s. Aborting the system startup." % msg)
			exit(-1)

		if self.dbcom.checkConnection() == ERROR:
			self.channel.close()
			self.log.LOG(LOG_CRITICAL, "sms.checkConnection()", "Failed to set the database connection. Aborting the system startup.")
			exit(-1)

		else:
			self.log.LOG(LOG_INFO, "sms", "Database access is OK.") 

		if self.dbcom.checkTables() == ERROR:
			self.channel.close()
			self.log.LOG(LOG_CRITICAL, "sms.checkConnection()", "Failed to check the default tables of the database. Aborting the system startup.")
			exit(-1)

		else:
			self.log.LOG(LOG_INFO, "sms", "Tables of the database are OK.") 
##
# Brief: Wait for subsytems connections (web interface, asterisk, alarms)
##
	def lookForConnection(self):

		while True:
			try:
				(client_channel, address) = self.channel.accept()
				self.log.LOG(LOG_INFO, "sms", "Client from %s has been connected." % str(address))

			except socket.error, emsg:
				self.log.LOG(LOG_ERROR, "sms.lookForConnection()", "lookForConnection()", "Failed to receive client connection. Error: %s" % str(emsg))
				continue
			try:
				cmsg = client_channel.recv(MSG_SIZE)
				result = self.processMessage(cmsg, client_channel)

				if result == OK:
					self.log.LOG(LOG_INFO, "sms.lookForConnection()", "Message from %s successfully processed." % str(address))
				elif result == ERROR:
					self.log.LOG(LOG_ERROR, "sms.lookForConnection()", "Message from %s can not be processed." % str(address))
				elif result == INVALID:
					self.log.LOG(LOG_INFO, "sms.lookForConnection()", "Unknow client attempted to send a command, but the package was dropped.")

				client_channel.close()

			except socket.error, emsg:
				self.log.LOG(LOG_ERROR, "sms.lookForConnection()", "Failed to receive client message. Error: %s" % emsg)
				continue
##
# Brief: Select client action package
# Param: cmsg The cient message package
# Return: OK if everything went right; INVALID if the client ID does not exist; ERROR if an error ocurred
##
	def processMessage (self, cmsg, client_channel):

			CID = self.shared.splitTag(cmsg, TAG_ID)
	
			if CID == ERROR:
				self.log.LOG(LOG_ERROR, "sms.processMessage()", "Failed to retrieve client ID from received message.")
				return ERROR

			if CID == WEB:
				self.log.LOG(LOG_INFO, "sms.processMessage()", "Message from WEB client was received.")
				self.doWebAction(cmsg, client_channel)
				return OK

			elif CID == ASTERISK:
				self.log.LOG(LOG_INFO, "sms.processMessage()", "Message from ASTERISK client was received.")
				return OK

			elif CID == ALARMS:
				self.doAlarmAction(cmsg, client_channel)
				self.log.LOG(LOG_INFO, "sms.processMessage()", "Message from ALARMS client was received.")
				return OK

			elif CID == MANAGER:
				self.log.LOG(LOG_INFO, "sms.processMessage()", "Message from MANAGER was received.")	
				self.doManagerAction(cmsg)

			else:
				self.log.LOG(LOG_INFO, "sms.processMessage()", "Received message has an invalid ID: %d" % CID)
				return INVALID
##
# Brief: Get de CMD from MANAGER message and process the action.
# Param: cmsg The message to be processed.
##
	def doManagerAction(self, cmsg):

		CMD = self.shared.splitTag(cmsg, TAG_CMD)
		
		if CMD == ERROR:
			self.log.LOG(LOG_ERROR, "sms.doManagerAction()", "Failed to retrieve the manager action from received message.")

		elif CMD == CMD_HALT:
			try:
				self.channel.close()
				self.log.LOG(LOG_INFO, "sms", "System is shutting down due to manager request.")
				exit(0)

			except socket.error, emsg:
				self.log.LOG(LOG_ERROR, "sms", "Failed to close socket connection. Halting anyway. Error: %s" % emsg)
				exit(-1)

		elif CMD == CMD_CLEAN_LOG:
			self.manager.actionCleanLog(self.log_path_list[SMS_LOGNAME])
			self.manager.actionCleanLog(self.log_path_list[DBCOM_LOGNAME])
			self.manager.actionCleanLog(self.log_path_list[ALARM_LOGNAME])

		elif CMD == CMD_SEND_SMS:
			pass
			#self.manager.actionScheduleAlarm(cmsg, dbcom)

		else:
			self.log.LOG(LOG_ERROR, "sms.doManagerAction()", "Received message has an invalid command: %s" % CMD)
##
# Brief: Process the WEB client messages.
##
	def doWebAction(self, cmsg, client_channel):

		CMD = self.shared.splitTag(cmsg, TAG_CMD)

		if CMD == CMD_LOGIN:
			answer = self.web.ActionLogin(cmsg)
			self.__sendMessage(client_channel, "%s" % RETURN[answer])
			client_channel.close()

		elif CMD == CMD_SEND_SMS:
			answer = self.manager.actionScheduleAlarm(cmsg, self.dbcom)
			self.__sendMessage(client_channel, "%s" % RETURN[answer])
			client_channel.close()

		else:
			self.log.LOG(LOG_ERROR, "sms", "Error while reading web request. Unknow command: %s" % CMD)			
			self.__sendMessage(client_channel, "%s" % RETURN[NOTFOUND])
			client_channel.close()
##
# Brief: Process the ALARMS requisitons.
##
	def doAlarmAction(self, cmsg, client_channel):

		CMD = self.shared.splitTag(cmsg, TAG_CMD)

		if CMD == CMD_BLOW:
			content = self.shared.splitTag(cmsg, TAG_CONTENT)
			destination = self.shared.splitTag(cmsg, TAG_PART, 0)
			counter = int(self.shared.splitTag(cmsg, TAG_FROM))

			answer = self.gsmcom.sendSMS(destination, content)
		
			if answer == OK: 
				self.dbcom.changeAlarmStatus(counter, SENT)

			elif answer == ERROR or answer == INVALID:
				self.dbcom.changeAlarmStatus(counter, FAILED)

			self.__sendMessage(client_channel, "%d" % answer)
			client_channel.close()

		else:
			self.log.LOG(LOG_ERROR, "sms", "Error while reading alarm request. Unknow command: %s:" % CMD)
			self.__sendMessage(client_channel, "%s" % ERROR)
			self.dbcom.changeAlarmStatus(counter, FAILED)
			client_channel.close()
##
# Brief: Send message in the channel.
# Param: channel The destination to the message.
# Param: msg The message to be sent.
# Return: OK if the message has be sent
##
	def __sendMessage(self, channel, msg):
		try:
			channel.send(msg)
			return OK
		except:
			self.log.LOG(LOG_ERROR, "sms", "Failed to send a message to the current client.")
			return ERROR

#---------------------------------------------------------#
# 			System start 			  #
#---------------------------------------------------------#
if __name__ == "__main__":

	bind_address = "127.0.0.1"
	bind_port = 3435
	log_path = "log"

	system = sms(bind_address, bind_port, log_path, GSM_ATCOM)
	system.start()
#---------------------------------------------------------#

