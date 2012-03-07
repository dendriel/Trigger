# -*-coding:utf-8-*-
from defines import *
import psycopg2
import psycopg2.extensions

class Pgcom:

    def __init__(self, db_host, db_user, db_pass, db_name, log_obj):
        """
        Brief: Initialize the database conection parameters.
        Param: db_host The ip where are the database.
        Param: db_user The user login to the databse.
        Param: db_pass The password for the user login.
        Param: db_name The database name pre-defined.
        Param: log A log objetct to register events.
        """
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_port = 5433
        self.log = log_obj
        self.conn = ''
        self.cursor = ''

    def start(self):

        try:
            self.conn = psycopg2.connect("\
            dbname=%s\
            user=%s\
            host=%s\
            port= %d\
            password=%s\
            " % (self.db_name, self.db_user, self.db_host, self.db_port, self.db_pass))
            self.cursor = self.conn.cursor()
            self.__query("lol")
            return OK

        except Exception, exc:
            #self.log.LOG(LOG_CRITICAL, "Pgcom.start()", "Erro ao se conectar a base de dados!");
            print"%s: %s" % (exc.__class__.__name__, exc)
            return ERROR

    def __query(self, query):

        try:
            self.cursor.execute("select *  from teste")
            print self.cursor.fetchall()
            return OK
        except Exception, exc:
            #self.log.LOG(LOG_CRITICAL, "Pgcom.start()", "Erro ao se conectar a base de dados!");
            print"%s: %s" % (exc.__class__.__name__, exc)
            return ERROR


    #método destrutor
    def __del__(self):
        print "Conexão finalizada!";
        del self;

#---------------------------------------------------------#
# 			System start 			  #
#---------------------------------------------------------#
if __name__ == "__main__":

    dbcom = Pgcom("localhost", "trigger", "trigger", "trigger", SYSTEM_LOG_PATH)
    dbcom.start()
#---------------------------------------------------------#
