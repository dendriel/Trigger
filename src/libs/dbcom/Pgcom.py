# -*-coding:utf-8-*-
import psycopg2
#from defines import *
#from slog import slog
from libs.defines.defines import *
import psycopg2.extensions

class Pgcom:

    def __init__(self, db_host, db_user, db_pass, db_name, db_port, log_obj):
        """
        Brief: Initialize the database conection parameters.
        Param: db_host The ip for connect with the DBMS.
        Param: db_user The user login to the databse.
        Param: db_pass The password for the user login.
        Param: db_name The database name.
        Param: db_port The DBMS port
        Param: log_obj A log objetct to register events.
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
        """
        Brief: Test the connection and parameters for database access.
        Return: OK if could establish a connection and access the database; ERROR otherwise.
        """
        if self.__connect() == ERROR:
            return ERROR

        elif self.__disconnect() == ERROR:
            return ERROR

        else:
            return OK

    def checkTables(self, user_tables):
        """
        Brief: Verifies that there are the standard tables and create it if there are no tables.
        """
        if len(user_tables) == 0:
            return OK

        if self.__connect() == OK:
            db_tables = self.__query("select relname from pg_stat_user_tables order by relname")

            # if there is no tables #
            if db_tables == NULL_LIST:
                db_tables = ()
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
                        self.log.LOG(LOG_CRITICAL, "dbcom", "Failed when creating table [%s] in the database." % user_tables[index])

            if self.__disconnect() == ERROR:
                self.log.LOG(LOG_CRITICAL, "dbcom", "Failed to disconnect from the DBMS.")
                return ERROR

            return OK

        else:
            return ERROR

    def registerRequisition(self, data):
        """
        Brief: Insert a new row for the new requisiton.
        Param: data The data for the new row.
        Return: OK if the new entry was successful inserted. ERROR if something went wrong.
        """
        if self.__connect() == OK:
            query = "INSERT INTO %s\
             (orig, dest, msg, oper, blow, stat) VALUES\
             ('%s', '%s', '%s', %d, '%s', %d)"\
             % (TABLE_SMS, data[DATA_ORG], data[DATA_DESTN], data[DATA_MSG], data[DATA_OPER], data[DATA_BLOW], ACTIVE)
            self.__query(query)

            if self.__disconnect() == ERROR:
                self.log.LOG(LOG_CRITICAL, "dbcom", "Failed to disconnect from the DBMS.")
                return ERROR

            self.log.LOG(LOG_INFO, "dbcom", "New register inseted into database. Table %s; Values: ('%s', '%s', '%s', %d, '%s', %d)"\
                      % (TABLE_SMS, data[DATA_ORG], data[DATA_DESTN], data[DATA_MSG], data[DATA_OPER], data[DATA_BLOW], ACTIVE))
            return OK

        else:
            return ERROR

    def getRequisitions(self, status):

        if self.__connect() == OK:
            query = "SELECT %s,%s,%s FROM %s WHERE stat=%d" % (DATA_ID, DATA_BLOW, DATA_SEND, TABLE_SMS, status)
            ret = self.__query(query)
            self.__disconnect()
            return ret

        else:
            return ERROR

    def changeRequisitionStatus(self, req_id, status):

        if self.__connect() == OK:
            query = "UPDATE %s SET %s=%d WHERE %s=%d" % (TABLE_SMS, DATA_STATUS, status, DATA_ID, req_id)
            ret = self.__query(query)
            self.__disconnect()
            return OK

        else:
            return ERROR

    def getDataFromRequisition(self, req_id):
        """
        brief: Retrive data from database to complete the requisition.
        Param: req_id The id to select the requisition.
        Return: A dictionay with the necessary data.
        """
        if self.__connect() == OK:
            query = "SELECT %s FROM %s WHERE %s=%d" % ((DATA_ORIG+","+DATA_DESTN+","+DATA_MSG), TABLE_SMS, DATA_ID, req_id)
            data = self.__query(query)
            self.__disconnect()
            # mount a dictionary with the data #
            data = data[0]
            req_dict = {DATA_ORIG:data[0].split()[0], DATA_DESTN:data[1].split(SEPARATOR_CHAR), DATA_MSG:data[2]}
            # remove blank spaces from dest field #
            req_dict[DATA_DESTN][len(req_dict[DATA_DESTN])-1] = req_dict[DATA_DESTN][len(req_dict[DATA_DESTN])-1][0:8]
            # remove blank spaces from orig field #
            return req_dict

        else:
            return ERROR

#--------------------------#
#    Private functions     #
#--------------------------#
    def __connect(self):
        """
        Brief: The functions must connect to the database before every access to him.
        Param: cursor_type This parameter defines the type of interaction that the object will have with the database.
        Return: OK if the connection was established; ERROR otherwise.
        """
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
        """
        Brief: Commit the changes and close the communication with the database.
        Return: OK if everything went fine; ERROR if any exception was caught.
        """
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return OK

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__disconnect()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def __query(self, query):
        """
        Brief: Send a query to the DBMS.
        Param: query The query to be sent.
        Return: What the DBMS returns for the query; INVALID if something went wrong.
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except psycopg2.ProgrammingError:
            return NULL_LIST

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__query()", "%s: %s" % (exc.__class__.__name__, exc))
            return INVALID

    def __createTable(self, table_type):
        """
        Brief: Create the specified table structure in database.
        Param: table_type The pre-defined type of the table that will be created. A list of the allowed tables are registered in the defines file.
        Return: OK if the table can be created; NOTFOUND if the specified table does not exist; ERROR if something went wrong.
        Note: This function will be used only at the system startup, when the system start checking if everything is OK and if they are in their places.
        """
        try:

            if table_type == TABLE_SMS:
                query = "CREATE TABLE %s (\
                     %s CHAR(7),\
                     %s CHAR(449),\
                     %s CHAR(150),\
                     %s INT,\
                     %s BOOLEAN,\
                     %s TIMESTAMP,\
                     %s INT,\
                     %s SERIAL PRIMARY KEY\
                );" % (TABLE_SMS, DATA_ORIG, DATA_DESTN, DATA_MSG, DATA_OPER, DATA_SEND, DATA_BLOW, DATA_STATUS, DATA_ID)

                self.cursor.execute(query)
                return OK

            else:
                return NOTFOUND

        except Exception, exc:
            self.log.LOG(LOG_CRITICAL, "dbcom.__createTable()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

#---------------------------------------------------------#
#         System start - Testing Purpose                  #
#---------------------------------------------------------#
if __name__ == "__main__":

    log = slog("./system.out")
    dbcom = Pgcom("localhost", "trigger", "trigger", "trigger", 5432, log)
    if dbcom.checkConnection() == OK:
        dbcom.checkTables((TABLE_SMS,))
        data = {DATA_ORG: "vitor",\
            DATA_MSG: "Mensagem de teste =)",\
            DATA_BLOW: "121220122050",\
            DATA_OPER: 1,\
            DATA_DESTN: "91663900,96075098,96500721,91683900,96770127"}
        dbcom.registerRequisition(data)
#---------------------------------------------------------#
