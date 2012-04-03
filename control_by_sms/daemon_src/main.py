#! /usr/bin/python
# -*-coding:utf-8-*-
import sys
from time import *
from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from libs.log.slog import slog
from libs.defines.defines import *
from libs.dbcom.Pgcom import Pgcom
from libs.gsmcom.Atcom import Atcom
from libs.manager.Manager import Manager

class trigger:

    def __init__(self, address, port, gsmcom_type):
        """
        Brief: Just initializes the system. Bind socket and stuff. :>
        Param: addres The IP to listen for connections;
        Param: port The port to listen for connections.
        Param: log The path to the log file.
        """
        self.address = address
        self.port = port

        try:
            self.log = slog(SYSTEM_LOG_PATH)
            self.dbcom = Pgcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT, self.log)

            if gsmcom_type == GSM_ATCOM:
                self.gsmcom = Atcom(log_obj=self.log, wport=MODULE_PORT)
            else:
                raise Exception

            self.manager = Manager(self.log, self.gsmcom)

        except Exception, exc:
            print "Failed to create one of the objects. %s: %s" % (exc.__class__.__name__, exc)
            sys.exit(0)

    def start(self):
        """
        Brief: Call all necessary functions and goes into the connection loop.
        """
        self.log.LOG(LOG_INFO, "system.start()", "Starting the system...")

        # Configure parameters and functions into XML-RPC Server #
        self.configureXMLRPCServer()

        # Test dbcom #
        self.checkDatabase()

        # Test gsmcom #
        self.testGsmCommunication()

        # Launch thread that will monitor SMS events #
        self.launchMonitorThread()

        self.log.LOG(LOG_INFO, "system.start()", "System started.")

        # Start to listening tcp socket #
        self.startXMLRPCServer()

        exit(0)


    def checkDatabase(self):
        """
        Brief: Check database and initialize his tables.
        """
        if self.dbcom.checkConnection() == ERROR:
            self.log.LOG(LOG_CRITICAL, "system.start.checkDatabase()", "Failed to set the database connection. Aborting the system startup.")
            exit(-1)

        elif self.dbcom.checkTables(DB_TABLES) == ERROR:
            self.log.LOG(LOG_CRITICAL, "system.start.checkDatabase()", "Failed to check the default tables of the database. Aborting the system startup.")
            exit(-1)

        else:
            self.log.LOG(LOG_INFO, "system.start()", "Tables of the database are OK.") 
            return

    def launchMonitorThread(self):
        """
        Brief: Try to launch Manager Thread. *The thread that will provide
              all the SMS services*
        """
        if self.manager.launchMonitor() != OK:
            self.log.LOG(LOG_CRITICAL, "system.start.launchMonitorThread()", "Failed to launch monitor thread. Halting...")
            sys.exit(0)

        else:
            self.log.LOG(LOG_INFO, "system.start()", "Manager thread launched.")
            return

    def testGsmCommunication(self):
        """
        Brief: Verify if the GSM Service is upline.
        """
        if self.gsmcom.testCommunication() != OK:
            self.log.LOG(LOG_CRITICAL, "system.start.testGsmCommunication()", "Failed to communicate with GSM module. Halting...")
            sys.exit(0)

        elif self.gsmcom.configureModule() != OK:
            self.log.LOG(LOG_CRITICAL, "system.start.testGsmCommunication()", "Failed to configure GSM module. Halting...")
            sys.exit(0)

        else:
            self.log.LOG(LOG_INFO, "system.start()", "GSM module is OK.")
            return

    def configureXMLRPCServer(self):
        """
        Brief: Configure and register functions into xml-rpc self.xmlrpc_server.
        """
        try:
            self.xmlrpc_server = SimpleXMLRPCServer((self.address, self.port))
            self.xmlrpc_server.register_function(self.newRequisition)
            self.xmlrpc_server.register_function(self.getRequisitions)
            self.xmlrpc_server.register_function(self.pingDaemon)
            #self.xmlrpc_server.register_function(self.systemHalt)
            self.xmlrpc_server.register_introspection_functions()
            self.log.LOG(LOG_INFO, "system.start()", "XML-RPC Server configured.")
            return

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "system.start.configureXMLRPCServer()", "Failed to configure XML-RPC Server parameters. %s: %s" % (exc.__class__.__name__, exc))
            exit(-1)

    def newRequisition(self, orig, destn, msg, oper, send, blow):
        """
        Brief: Treat data and try to insert new register into the database.
        Param: orig The name that identifies the origin;
        Param: destn The destinations of the requisition;
        Param: msg The message content;
        Param: oper The preferred operator to be used;
        Param: send If the requisition is to be sent as fast as possible;
        Param: blow When the requisition will be sent.
        Return: OK(0) if could register the requisition; ERROR(-1) otherwise.
        """
        try:
            data_dict = {DATA_ORIG: orig,\
                         DATA_DESTN: destn,\
                         DATA_MSG: msg,\
                         DATA_OPER: oper,\
                         DATA_SEND: send,\
                         DATA_BLOW: blow}

            if self.dbcom.registerRequisition(data_dict) == OK:
                self.log.LOG(LOG_INFO, "system", "New requisition from RPC was registered.")
                return OK

            else:
                self.log.LOG(LOG_ERROR, "system.newRequisition()", "Failed to insert new requisition from RPC.")
                return ERROR

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "system.newRequisition()", "Failed to insert new requisition from RPC connection. %s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def getRequisitions(self, status):
        """
        Brief: Ask database by a list of the specified requisition status.
        Param: status The status for searching for the requisitions.
        Return: An list with the ocurrence of the specified requisition status.
        """
        req_list = self.dbcom.getRequisitions(status)
        return req_list

    def pingDaemon(self):
        """
        Brief: To look after daemon status.
        Return: OK(0).
        """
        return OK

    def systemHalt(self):
        """
        Brief: Halt the system.
        """
        self.log.LOG(LOG_INFO, "system", "Halting system due RPC requisition.")
        # TODO does not work... yet. #
        #exit(0)
        return OK

    def startXMLRPCServer(self):
        """
        Brief: Start to listening connections into the self.xmlrpc_server.
        Return: None.
        """
        try:
            self.log.LOG(LOG_INFO, "system.start()", "XML-RPC Server started binded into %s:%d" % (self.address, self.port))
            self.xmlrpc_server.serve_forever()

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "system.start.startXMLRPXServer()", "Failed to start XML-RPC Server. %s: %s. Halting..." % (exc.__class__.__name__, exc))
            exit(-1)
        

#---------------------------------------------------------#
#             System bootstrap                            #
#---------------------------------------------------------#
if __name__ == "__main__":

    bind_address = "192.168.0.155"
    bind_port = SYSTEM_PORT
    system = trigger(bind_address, bind_port, GSM_ATCOM)
    system.start()
#---------------------------------------------------------#
