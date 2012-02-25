#coding=utf-8
import socket
from time import sleep
from libs.defines.defines import *

class Amicom:
##
# Brief: set some parameters and set the family parameters for the socket channel
##
	def __init__(self, log, address="127.0.0.1", port="5038"):
		self.log = log
		self.ast_address = address
		self.ast_port = port
		self.channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##
# Brief: Connect to Manager Interface from Asterisk in specified (in __init__) port/address
# Return: OK if the channel was stablished; ERROR if something went wrong.
##
	def startCom(self):
		try:
			self.channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.channel.connect( (self.ast_address, self.ast_port) )
			self.log.LOG(LOG_CRITICAL, "startCom()", "The channel with the Asterisk Manager Interface was established.")
			return OK
		except socket.error, msg:
			self.log.LOG(LOG_CRITICAL, "startCom()", "Error while connecting to Asterisk Manager Interface. Error <%s>" % msg)
			self.channel.close()
			return ERROR
##
# Brief: Just close the channel stream
# Return: OK if everything went fine; ERROR if the channel can not be closed.
##
	def closeCom(self):
		try:
			self.channel.close()
			return OK
		except socket.error, msg:
			self.log.LOG(LOG_ERROR, "closeCom()", "Error while closing the Asterisk Manager stream. Error <%s>" % msg)
			self.channel.close()
			return ERROR
##
# Brief: Receive the events from the manager interface. We do not need that just now. In future
#	implementations we could design some functions to filter the data received, and get a
#	more acurrate feedback for the core
# Return: The content received in the AMI channel; ERROR if something went wrong.
##
	def readEvents(self):
		try:
			content = self.channel.recv(MSG_SIZE)
			return content
		except socket.error, msg:
			self.log.LOG(LOG_ERROR, "readEvents()", "Error while scanning the channel for received messages. Error <%s>" % msg)
			self.channel.close()
			return ERROR
##
# Brief: This function sends data in the open stream. The pre-modeled packages.
# Param: action The package pre-modeled by the caller function.
# Return: OK if everything went fine; ERROR if something went wrong.
##
	def sendAction(self, action):
		try:
			self.channel.send(action)	
			return OK
		except socket.error, msg:
			self.log.LOG(LOG_ERROR, "sendAction()", "Error when trying to send data in the AMI channel. Error <%s>" % msg)
			self.channel.close()
			return ERROR
##
# Brief: Seek for specific events in the data buffer.
# Param: target The buffer to be searched.
# Param: events The string to be found in the buffer.
# Return: OK If the buffer contain the string; NOTFOUND if
#	there is no the specified string in the buffer. 
# Note: Maybe this function is not necessary. #
##
    def lookFor(self, target, events=""):
        if events.find(target) > -1:
            return OK
        else:
            return NOTFOUND
##+++++++++++++++++++++++##
# List of allowed Actions #----------------------------------------------------<>
##+++++++++++++++++++++++##

##
# Brief: This is the login action. It is needed to be send before any other actions.
# Param: username The pre-configured allowed user in /etc/asterisk/manager.conf; this 
#	parameter is defined in the defines file.
# Param: secret The same of above. But is the password for the user.
# Param: events This is usefull for implementing the filter events part.
# Return: OK if everything went fine; ERROR if something went wrong.
##
	def login(self, username, secret, events):
		action = "Action: Login\r\nUsername: %s\r\nSecret: %s\r\nEvents: %s\r\n\r\n" % (username, secret, events)

		if self.sendAction(action) == OK:
			events =  self.readEvents()
			if self.lookFor("Response: Success\r\nMessage: Authentication accepted", events) == OK:
				return OK
			else:
				return NOTFOUND
		else:
			return ERROR
##
# Brief: Disconnect the interface
# Return: OK if everything went fine; ERROR if something went wrong.
##
	def logoff(self):
		action = "Action: logoff\r\n\r\n"

		if self.sendAction(action) == OK:
			events =  self.readEvents()
			if self.lookFor("Response: Goodbye\r\nMessage: Thanks for all the fish.", events) == OK:
				return OK
			else:
				return NOTFOUND
		else:
			return ERROR
##
# Brief: Just a prototype for the "sendSMS" action (not implemented in every Asterisk server)
##
	def sendSms(self, org, dest, content):
		action = "Action: sendSms........"
		action = "OK" # for testing purpose #
		if self.sendAction(action) == OK:
			return OK
		else:
			return ERROR
