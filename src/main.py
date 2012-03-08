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
from libs.manager.Manager import Manager
from interfaces.Web import Web

class trigger:

    def __init__(self, address, port, gsmcom_type):
        """
        Brief: Just initializes the system. Bind socket and stuff. :>
        Param: addres The IP to listen for connections.
        Param: port The port to listen for connections.
        Param: log The path to the log file.
        """
        self.address = address
        self.port = port
        self.channel = '' 
        
        try:
            self.log = slog(SYSTEM_LOG_PATH)
            self.dbcom = dbcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, SYSTEM_LOG_PATH)
            self.manager = manager(self.log)
            
            if gsmcom_type == GSM_ATCOM:
                self.gsmcom = Atcom(SYSTEM_LOG_PATH, SYSTEM_LOG_PATH)
            
            elif gsmcom_type == GSM_ASTERISK:
                raise Exception
            
            else:
                raise Exception
        
        except:
        	print "Failed to create one of the objects."
        	sys.exit(0)

    def start(self):
        """
        Brief: Call all necessary functions and goes into the connection loop
        """
        self.log.LOG(LOG_INFO, "sms", "Starting the system.")
        self.checkConnection()

        # Launch thread that will monitor SMS events #
        self.manager.manageSmsEvents()
        self.log.LOG(LOG_INFO, "sms", "Manager thread launched.")

        # Test dbcom #
        #self.checkDatabase()
        
        self.log.LOG(LOG_INFO, "sms", "System started.")
        self.lookForConnection()
        self.channel.close()

        sys.exit(0)

    def checkConnection(self):
        """
        Brief: Set the system connection and bind to
        Return: OK if everything went fine; Or halt the system if unsucess
        """
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

    def checkDatabase(self):

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
            return

    def lookForConnection(self):
        """
        Brief: Wait for subsytems connections.
        """
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

    def processMessage (self, cmsg, client_channel):
        """
        Brief: Select client action package
        Param: cmsg The cient message package
        Return: OK if everything went right; INVALID if the client ID does not exist; ERROR if an error ocurred
        """
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








#---------------------------------------------------------#
# 			System start 			  #
#---------------------------------------------------------#
if __name__ == "__main__":

    bind_address = "127.0.0.1"
    bind_port = 3435
    system = trigger(bind_address, bind_port, GSM_ATCOM)
    system.start()
#---------------------------------------------------------#