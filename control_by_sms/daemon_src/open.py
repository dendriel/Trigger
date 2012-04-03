import subprocess
import time

path = "./validation.php"
interpreter = "php"

number = "91553900"
db_name = "moodle"
user = "moodle"
password = "moodle"

val = subprocess.Popen([interpreter, path, number, db_name, user, password]);

print val.wait()
