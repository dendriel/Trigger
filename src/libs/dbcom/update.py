import sys
import MySQLdb

try:
        conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "sample_sms_database")

except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

cursor = conn.cursor()

try:
	cursor.execute ("""
		UPDATE animal SET name = %s
		WHERE name = %s
		""", ("snake", "turtle"))
	print "Number of rows updated: %d" % cursor.rowcount

except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

cursor.close()
conn.close()

