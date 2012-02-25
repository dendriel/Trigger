 # -*- coding: UTF-8 -*-
import sys
import serial
from time import sleep
from mx.DateTime import now
from libs.defines.defines import *
from libs.log.slog import slog

TIME_BETWEEN_AT = 0.2

class Atcom:

##
# Brief: Set global parameters that will be 
#		used by the most part of the functions.
##
	def __init__(self, wport="/dev/ttyACM0", bitrate="115200", logname="./gsmcom.log", atLogPath="", mtype="default"):

		self.wport = wport
		self.bitrate = bitrate
		self.mtype = mtype
		self.log = slog(logname)
		self.atlog = slog("%s/atcom.log" % atLogPath)
		self.serial = ''
##
# Brief: Open a serial port to communicate with the module.
##
	def _open_port (self):

		try:
			self.serial = serial.Serial(self.wport, self.bitrate, timeout=1)
			return OK

		except IOError, emsg:
			self.log.LOG(LOG_CRITICAL, "gsmcom._open_port()", "An error occurred when opening %s port with %s of bitrate. Error: %s" % (self.wport, self.bitrate, emsg))
			return ERROR
##
# Brief: Close the communication serial port.
##
	def _close_port(self):
		try:
			self.serial.close()
			return OK
		except IOError, emsg:
			self.log.LOG(LOG_ERROR, "gsmcom", "Attempt to close the serial port failed. Error: %s" % emsg)
			return ERROR
##
# Brief: Read content of serial buffer.
# Return: The data of the serial buffer if exist; 
#	ERROR if something went wrong.
##
	def _read(self):
		try:
			msg = ""
			while(self.serial.inWaiting() > 0):
				msg += self.serial.readline()
			return msg

		except IOError, emsg:
			self.log.LOG(LOG_ERROR, "gsmcom._read()", "An error occurred while reading the serial buffer. Error: %s" % emsg)
			return ERROR
##
# Brief: Send content in serial buffer.
# Param: msg The content to be sent.
# Return: OK if the command was sent; ERROR if
#	something went wrong.
##
	def _send(self, msg):
		
		try:
			self.serial.write(msg+'\r')
			sleep(TIME_BETWEEN_AT)

		except IOError, emsg:
			self.log.LOG(LOG_ERROR, "gsmcom._send()", "An error occurred when sending data in the serial buffer.")
			return ERROR

		self.atlog.LOG(LOG_INFO, "gsmcom", "Command sent: %s\n" % msg)	
		# get response # * the answer is taking too long
		# uncomment the lines bellow to register the module answers
		#r_msg = self.read()
		#self.log("Answer:\n %s\n" % r_msg, "%s" % now())
		return OK
##
# Brief: Print the chosen parameters to be used.
##
	def info (self):
		print "Valores utilizados: %s %s %s %s" % (self.wport, self.bitrate, self.logname, self.mtype)
		return
	
###########################
# Specific functions	  #
###########################
##
# Brief: Send initializing commands to the module
##
	def initModule(self):
		pass
##
# Brief: Send a sms.
# Param: destination The destination extension to were
#	the sms will be sent.
# Param: content The message that the sms will load.
# Return: OK if the alarm was sent; ERROR in whatever
#	other case.
##
	def sendSMS(self, destination, content):

		if self._open_port() == ERROR:
			return ERROR
		
		# Clear the content of the rx buffer #
		self._read()
		# Setting something important #
		self._send("AT+CMGF=1")
		# Starting the command #
		self._send("AT+CMGS=\"%s\"" % destination)
		# Writing the content #
		self._send("%s" % content)
		# Confirm the command #
		self._send("\032")

		answer = self._read()

		if answer.find("ERROR") > 0: #|| answer.find("+CMGS: 73") < 0:
			self.atlog.LOG(LOG_ERROR, "gsmcom.sendSMS()", "Unexpected answer from module. Content: %s" % answer)
			return INVALID

		self.atlog.LOG(LOG_INFO, "gsmcom.sendSMS()", "Answer: %s" % answer)

		self._close_port()
		return OK
