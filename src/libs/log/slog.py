#################################################################
#  This is a funny module, because if he stop for any reason,   #
# we will lost our way to know what is happening in the system. #
# Then, do not mess this up!					#
#################################################################

from libs.defines.defines import *
from libs.shared.shared import shared

class slog:

##
# Brief: start the object and define the log file path
# Param: directory The log file path, the log name is defined in libs.include.include
##	
	def __init__(self, directory):
		self.directory = directory
		self.shared = shared()

##
# Brief: create a log message with date, level, name of the caller function and any content.
# Param: level The warning level of the log message.
# Param: callerName The name of the function that is asking for the log.
# Param: content The message to logging.
# Return: OK if the message was logged; ERROR if there are any error.
##
	def LOG(self, level, callerName, content):
		try:
			# makeDate #
			path = "%s" % (self.directory)
			file = open(path, "a")
			
			if level == LOG_INFO:
				lmsg = "INFO"
			elif level == LOG_ERROR:
				lmsg = "ERROR"
			elif level == LOG_CRITICAL:
				lmsg = "CRITICAL"

			file.write("%s - LOG LEVEL %s -- from %s -- message: %s\n" % (self.shared.makeTime(), lmsg, callerName, content))
			file.close()

			return OK

		except IOError as (errno, strerror):
			print "I/O error({0}): {1}".format(errno, strerror)
			return ERROR
##
# Brief: clean all the content of the log file.
# Return: OK if the message was logged; ERROR if there are any error.
##
	def CLEAN(self, path):
		try:
			file = open(path, "w")
			file.close()

			return OK

		except IOError as (errno, strerror):
			print "I/O error({0}): {1}".format(errno, strerror)
			return ERROR

	# maybe put in shared libs #
	def makeDate():
		pass
