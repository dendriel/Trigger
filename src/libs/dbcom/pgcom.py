# -*-coding:utf-8-*-
from defines import *
import psycopg2

class Pgcom:


    def __init__(self, db_host, db_user, db_pass, db_name, log_path):
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
      #  self.log = slog(log_path)
        self.com = ''
        self.cursor = ''

    def start(self):

        try:
            conn = psycopg2.connect("\
            dbname='trigger'\
            user='trigger'\
            host='127.0.1.1'\
            password='trigger'\
            ");
            self.cur = conn.cursor();
            
        except:
            print "Erro ao se conectar a base de dados!";

    #método destrutor
    def __del__(self):
        print "Conexão finalizada!";
        del self;

#---------------------------------------------------------#
# 			System start 			  #
#---------------------------------------------------------#
if __name__ == "__main__":

    dbcom = Pgcom(DB_HOST, DB_USER, DB_PASS, DB_NAME, SYSTEM_LOG_PATH)
    dbcom.start()
#---------------------------------------------------------#
