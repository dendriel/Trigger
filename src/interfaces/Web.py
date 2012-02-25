from libs.defines.defines import *
from libs.shared.shared import shared
from libs.log.slog import slog

class Web:

	def __init__(self, log, dbcom):
		self.log = slog(log)
		self.shared = shared()
		self.dbcom = dbcom

##
# Brief: Make the authentication of the user.
##
        def ActionLogin(self, cmsg):

                        user = self.shared.splitTag(cmsg, TAG_FROM)
                        passwd = self.shared.splitTag(cmsg, TAG_CONTENT)

                        if user == ERROR or passwd == ERROR:
                                self.log.LOG(LOG_ERROR, "sms.doWebAction()","Error while retrieving the login/password content from the data package.")
                                return
                        elif user == NOTFOUND or passwd == NOTFOUND:
                                self.log.LOG(LOG_ERROR, "sms.doWebAction()","One or more TAGs are missing in the data package. Authentication failed.")
                                return
                        else:
                                ret = self.dbcom.validateLogin(user, passwd)

                                if ret == OK:
                                        self.log.LOG(LOG_INFO, "sms", "User %s has been authenticated." % user)
                                        return OK

                                elif ret == INVALID:
                                        self.log.LOG(LOG_INFO, "sms", "Authetication for user \"%s\" failed. Password incorrect." % user)
                                        return INVALID

                                elif ret == ERROR:
                                        self.log.LOG(LOG_ERROR, "sms", "An error ocurred when authenticating an user.")
                                        return ERROR

                                elif ret == NOTFOUND:
                                        self.log.LOG(LOG_INFO, "sms", "Authentication for user \"%s\" failed. User doesn't exist." % user)
                                        return NOTFOUND
                                else:
                                        self.log.LOG(LOG_ERROR, "sms.webAtcionLogin()", "Unknow answer from dbcom.validateLogin.")
					return ERROR

