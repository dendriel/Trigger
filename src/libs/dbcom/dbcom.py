# -*-coding:utf-8-*-
import sys
import MySQLdb
import MySQLdb.cursors
from libs.defines.defines import *
from libs.log.slog import slog

class dbcom:

##
# Brief: Initialize the database conection parameters.
# Param: db_host The ip where are the database.
# Param: db_user The user login to the databse.
# Param: db_pass The password for the user login.
# Param: db_name The database name pre-defined.
# Param: log A log objetct to register events.
##
	def __init__(self, db_host, db_user, db_pass, db_name, log_path):

		self.db_host = db_host
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_name = db_name
		self.log = slog(log_path)
		self.com = ''
		self.cursor = ''
##
# Brief: Test the connection and parameters for
#	database access.
# Return: OK if could establish a connection and
#	access the database; ERROR otherwise.
##
	def checkConnection(self):

		if self.__connect() == ERROR:
			return ERROR
		elif self.__disconnect() == ERROR:
			return ERROR
		else:
			return OK
##
# Brief: Verifies that there are the standard tables
#	and create it if there are no tables.
# Note: In every table, when created, is inserted
#	a default row, this function uses
#	that fact to test the tables.
##
	def checkTables(self):

		self.__connect()

		if self.__createTable(TABLE_USER) == ERROR:
			return ERROR
		elif self.__createTable(TABLE_SMS) == ERROR:
			return ERROR

		self.__disconnect()
		return OK
##
# Brief: Validate de login and password to get
#	access to the system.
# Param: user The login name to be validated.
# Param: passwd The password to be validated.
# Return: OK If the user exist and the password
#	is correct; NOTFOUND If the username 
#	does not exist; INVALID if the password
#	is incorrect; ERROR if there is an error.
##
	def validateLogin(self, user, passwd):

		content = self.__retrieve(TABLE_USER, "login, passwd")
		if content == ERROR:
			return ERROR
		else:
			for row in content:

				if user == row["login"]:
					if passwd == row["passwd"]:
						return OK
					else:
						return INVALID
			return NOTFOUND
##
# Brief: Register a SMS in the database.
# Param: orig Who are requesting the service.
# Param: dest Who is going to receive de SMS.
# Param: When the SMS will be sent.
# Param: oper A flag to select the best operator
#	to send the SMS.
# Param: msg The content that will be sent in the
#	SMS.
# Param: stat The status of the alarm (defined
#	in defines.py)
# Return: OK if the alarm was registered; ERROR
#	if a problem has ocurred.
##
	def registerAlarm(self, orig, dest, blow, oper, msg, stat):

		answer = self.__insert(TABLE_SMS, "(orig, dest, msg, oper, blow, stat)", "('%s', '%s', '%s', '%d', '%s', '%d')" % (orig, dest, msg, oper, blow, stat))
		return answer
##
# Brief: Change the status of an Alarm.
# Param: identifier The counter number that the database
#	automaticlly inserts into the table.
# Return: OK if the alarm status could be changed; 
#	ERROR if something went wrong.
# Note: Adapt to interpret the mysql error and add "NOTFOUND 
#	if the alarm does not exist;"
##
	def changeAlarmStatus(self, identifier, new_status):

		answer = self.__update(TABLE_SMS, "stat = %d" % new_status, "count = %d" % identifier)
		return answer
##
# Brief: Search for the last alarm inserted into the table.
# Return: The most higher counter found in the table.
##
	def getHigherCounter(self):

		counters_list = self.__retrieve(TABLE_SMS, "count")

		higher = -1
	
		for it in counters_list:
			if it['count'] > higher:
				higher = it['count']

		return higher
##
# Brief: Create specified table structure in database.
# Param: table_type The pre-defined type of the table
#	that will be created in the database. A list
#	of the allowed tables are registered in the
#	defines file.
# Return: OK if the table can be created; NOTFOUND if
#	the specified table does not exist; ERROR if
#	something went wrong.
# Note: This function will be used only at the system
#	startup, when the system start checking if
#	everything is OK and are in their places.
##
	def __createTable(self, table_type):

		try:
			if table_type == TABLE_USER:
				try:
					self.cursor.execute("""
							CREATE TABLE IF NOT EXISTS %s
							(
								login		CHAR(20),
								ramal		CHAR(20),
								passwd		CHAR(20),
								access		INT,
								count		INT NOT NULL AUTO_INCREMENT,
								PRIMARY KEY	(count)
							)
							""" % TABLE_USER)
					self.log.LOG(LOG_INFO, "dbcom","Table \"user\" validated.") 
					return OK
				except:
					print "caiu na except!"

			if table_type == TABLE_SMS:
				self.cursor.execute("""
							CREATE TABLE IF NOT EXISTS %s
							(
								orig		CHAR(8),
								dest		CHAR(12),
								msg		CHAR(150),
								oper		INT,
								blow		CHAR(12),
								stat		INT,
								count		INT NOT NULL AUTO_INCREMENT,
								PRIMARY KEY	(count)
							)
							""" % TABLE_SMS)
				self.log.LOG(LOG_INFO, "dbcom","Table \"sms\" validated.") 
				return OK

			else:
				self.log.LOG(LOG_ERROR, "dbcom.createTable()", "Failed when creating a new table in the database. The specified table aren't registered.")
				return ERROR

		except MySQLdb.Error, msg:
			self.log.LOG(LOG_ERROR, "dbcom.createTable()", "Failed while creating a new table in the database. Error: %d: %s" % msg.args)
			return ERROR
##
# Brief: The functions must connect to the database
#	before every access to him.
# Param: cursor_type This parameter defines the type of
#	interaction that the object will have with the
#	database.
# Return: OK if the connection was established; ERROR otherwise.
##
	def __connect(self, cursor_type=MySQLdb.cursors.Cursor):

		try:
			self.com = MySQLdb.connect(host = self.db_host, 
						   user = self.db_user, 
						   passwd = self.db_pass, 
						   db = self.db_name)
			self.cursor = self.com.cursor(cursor_type)
			return OK

		except MySQLdb.Error, msg:
                        self.log.LOG(LOG_CRITICAL, "dbcom.__connect()"," Failed to connect to the database. Error: %d: %s" % msg.args)
			return ERROR
##
# Brief: Commit the changes and close the communication
#	with the database.
# Return: OK if everything went fine; ERROR if any exception
#	was caught.
##
	def __disconnect(self):

		try:
			self.cursor.close()
			self.com.commit()
			self.com.close()
			return OK
	
		except MySQLdb.Error, msg:
                        self.log.LOG(LOG_ERROR, "dbcom"," Failed to stop communication with the database. Error: %d: %s" % msg.args)
			return ERROR
##
# Brief: Retrieve all the content of the specified table.
# Param: content The columns to be recovered.
# Param: table The table to be searched.
# Return: A dictionary with the solicited data; ERROR if
#	anything went wrong.
##
	def __retrieve(self, table, content):

		if self.__connect(cursor_type=MySQLdb.cursors.DictCursor) == ERROR:
			return ERROR

		query = "SELECT %s FROM %s" % (content, table)
		try:
			self.cursor.execute(query)

		except MySQLdb.Error, msg:
                        self.log.LOG(LOG_ERROR, "dbcom"," Failed to retrieve content from database. Error: %d: %s" % msg.args)
			return ERROR

		self.log.LOG(LOG_INFO, "dbcom", "Query executed to the database: %s" % query)
		content = self.cursor.fetchall()
		self.__disconnect()
		return content 
##
# Brief: Insert the specified content in the selected table.
# Param: table The table to be inserted content.
# Param: fields The columns that will receive data.
# Param: content The content that will be sent to the database.
# Return: OK if the content has been sent; ERROR otherwise.
##
	def __insert(self, table, fields, values):

		if self.__connect() == ERROR:
			return ERROR

		query = "INSERT INTO %s %s VALUES %s" % (table, fields, values)
		try:
			self.cursor.execute(query)

		except MySQLdb.Error, msg:
                        self.log.LOG(LOG_ERROR, "dbcom"," Failed to insert content into the database. Error: %d: %s" % msg.args)
			return ERROR

		self.log.LOG(LOG_INFO, "dbcom", "Query executed to the database: %s" % query)

		self.__disconnect()
		return OK
##
# Brief: Update information in the specified table.
# Param: table The table to be updated.
# Param: new_content The content that will be inserted.
# Param: ref The reference for the tuple where the the
#	content will be changed.
# Return: OK if the content could be changed; ERROR if
#	something went wrong.
##
	def __update(self, table, new_content, ref):

		if self.__connect() == ERROR:
			return ERROR

		query = "UPDATE %s SET %s WHERE %s" % (table, new_content, ref)
		try:
			self.cursor.execute(query)

		except MySQLdb.Error, msg:
                        self.log.LOG(LOG_ERROR, "dbcom"," Failed to update content from database. Error: %d: %s" % msg.args)
			return ERROR

		self.log.LOG(LOG_INFO, "dbcom", "Query executed to the database: %s" % query)
		self.__disconnect()
		return OK
