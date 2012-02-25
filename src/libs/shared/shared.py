#coding=utf8
from mx.DateTime import DateTime
from datetime import datetime
from libs.defines.defines import *

class shared:

##
# Brief: truely no one. But is good that the function is here, 
#       because of future date/time processing.
# Return: a string with the date and time at this moment.
##
	def makeTime(self):
		return datetime.now()
##
# Brief: Retrieves the tag content.
# Param: cmsg The data package to get the content.
# Param: tag The TAG to be splitted.
# Return: The content of the tag; ERROR if something went
#	 wrong; NOTFOUND if the specified TAG does not exist. 
# Note: Yeap, there is a more efficient way to do that. Using more generic functions.
##
	def splitTag(self, cmsg, tag, part=0):
		try:
			if tag == TAG_ID:
	                        start = cmsg.find('\ID:')
        	                end = cmsg.find('/ID')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return int(cmsg[ (start+4):end ])

			elif tag == TAG_CMD:
                        	start = cmsg.find('\CMD:')
	                        end = cmsg.find('/CMD')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
				else:
                                	return (cmsg[ (start+5):end ])

			elif tag == TAG_DATA:
                        	start = cmsg.find('\DATA:')
	                        end = cmsg.find('/DATA')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return (cmsg[ (start+6):end ])

			elif tag == TAG_FROM:
                        	start = cmsg.find('\FROM:')
	                        end = cmsg.find('/FROM')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return (cmsg[ (start+6):end ])

			elif tag == TAG_CONTENT:
                        	start = cmsg.find('\CONTENT:')
	                        end = cmsg.find('/CONTENT')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return (cmsg[ (start+9):end ])

			elif tag == TAG_HOWMANY:
	                        start = cmsg.find('\HOWMANY:')
        	                end = cmsg.find('/HOWMANY')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return int(cmsg[ (start+9):end ])

			elif tag == TAG_BLOW:
	                        start = cmsg.find('\BLOW:')
        	                end = cmsg.find('/BLOW')
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return cmsg[ (start+6):end ]

			elif tag == TAG_PART:
	                        start = cmsg.find('\PART%d:' % part)
        	                end = cmsg.find('/PART%d' % part)
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return cmsg[ (start+7):end ]

			elif tag == TAG_INFO:
                        	start = cmsg.find('\INFO%d:' % part)
	                        end = cmsg.find('/INFO%d' % part)
	
        	                if ( start <= -1 or end <= -1 ):
                	                return NOTFOUND
                        	else:
                                	return (cmsg[ (start+7):end ])
			else:
				return ERROR

		except:
			return ERROR
##
# Brief: Mount a mxDateTime object from a string.
# Param: time_str The string that have the content
#	to mount the time object.
# Return: The mxDateTime object; NOTFOUND if some
#	content are missing; ERROR if something
#	goes wrong.
# Note: the parameter time_str must be in the
#	following format: daymonthyearhourminute;
#	ex.: time_str = "241220122359" that's means
#	24, december, 2012, 23 hours and 59 minutes.
##
	def mountTime(self, time_str):

		dic_time = {"day":0, "month":0, "year":0, "hour":0, "minute":0}

		dic_time["day"] = int(time_str[0:2])
		dic_time["month"] = int(time_str[2:4])
		dic_time["year"] = int(time_str[4:8])
		dic_time["hour"] = int(time_str[8:10])
		dic_time["min"] = int(time_str[10:12])

		ret = self._validateTime(dic_time)

		if ret == OK:
			time = DateTime(dic_time["year"], dic_time["month"], dic_time["day"], dic_time["hour"], dic_time["min"], 0)
			return time
		else:
			return INVALID
##
# Brief: Validate time values.
# Param: dic_time The dictionary to validate.
# Return: OK if the time is right: INVALID if
#	the some of the values are out of bound.
##
	def _validateTime(self, dic_time):

		if dic_time["day"] < 0 or dic_time["day"] > 31:
			return INVALID

		elif dic_time["month"] < 1 or dic_time["month"] > 12:
			return INVALID

		elif dic_time["year"] < 1000:
			return INVALID

		elif dic_time["hour"] < 0 or dic_time["hour"] > 23:
			return INVALID

		elif dic_time["minute"] < 0 or dic_time["minute"] > 59:
			return INVALID

		else:
			return OK

