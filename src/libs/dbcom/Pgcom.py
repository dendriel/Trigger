# -*-coding:utf-8-*-
import psycopg2
from libs.defines.defines import *
#import psycopg2.extensions

class Pgcom:

    def __init__(self, db_host, db_user, db_pass, db_name, db_port, log_obj):
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
        self.db_port = db_port
        self.log = log_obj
        self.conn = ''
        self.cursor = ''

    def checkConnection(self):

        if self.__connect() == ERROR:
            return ERROR

        elif self.__disconnect() == ERROR:
            return ERROR

        else:
            return OK

    def checkTables(self, user_tables):

        if len(user_tables) == 0:
            return OK

        if self.__connect() == OK:

            db_tables = self.__query("select relname from pg_stat_user_tables order by relname")

            # if there is no tables #
            if db_tables == ERROR:
                db_tables = 'none'
                return OK
            else:
                db_tables = db_tables[0]

            for index in range(len(user_tables)):

                present = False
                for db_index in range(len(db_tables)):

                    if user_tables[index] == db_tables[db_index]:
                        present = True
                        break

                if present == False:

                    ret = self.__createTable(user_tables[index])

                    if ret == OK:
                        self.log.LOG(LOG_INFO, "dbcom","Table \"%s\"  was created." % user_tables[index])

                    elif ret == NOTFOUND:
                        self.log.LOG(LOG_ERROR, "dbcom", "Failed when creating a new table in the database. The specified table [%s] aren't registered." % table_type)

                    else:
                        self.log.LOG(LOG_CRITICAL, "dbcom", "Failed when creating a new table in the database.")

            self.__disconnect()
            return OK


        else:
            return ERROR

#--------------------------#
#    Private functions     #
#--------------------------#
    def __connect(self):

        try:
            self.conn = psycopg2.connect("\
            dbname=%s\
            user=%s\
            host=%s\
            port=%d\
            password=%s\
            " % (self.db_name, self.db_user, self.db_host, self.db_port, self.db_pass))
            self.cursor = self.conn.cursor()
            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__connect()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def __disconnect(self):

        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__disconnect()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def __query(self, query):

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__query()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR


    def __createTable(self, table_type):

        try:

            if table_type == TABLE_SMS:
                query = "CREATE TABLE %s (orig CHAR(8), dest CHAR(12), msg CHAR(150), oper INT, blow CHAR(12), stat INT, count SERIAL PRIMARY KEY);" % (TABLE_SMS)
                self.cursor.execute(query)
                return OK
    
            else:
                return NOTFOUND

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__createTable()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

#---------------------------------------------------------#
#         System start    #
#---------------------------------------------------------#
if __name__ == "__main__":

    log = slog("./system.out")
    dbcom = Pgcom("localhost", "trigger", "trigger", "trigger", 5433, log)
    dbcom.checkConnection()
    dbcom.checkTables((TABLE_SMS,))
#---------------------------------------------------------#
