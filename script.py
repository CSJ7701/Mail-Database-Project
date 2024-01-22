

import sqlite3

MailDB = sqlite3.connect("MailDB")
Mail = MailDB.cursor()
test=Mail.execute("SELECT * FROM Cadets")
print(test.fetchall())
