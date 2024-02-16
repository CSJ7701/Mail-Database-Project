import sqlite3
import os

class Database:
    def __init__(self, db_name):
        self.db_name=db_name
        print(self.db_name)
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor

    def add_package(self, box, track):
        name, email=self.get_cadet_info(box)
        date=datetime.today().strftime('%Y%b%d')
        self.cursor.execute("INSERT INTO packages(tracking_number, adressee, received) VALUES (?, ?, ?)", (track, name, date))
        self.conn.commit()

    def find_in_db(self, var):
        self.cursor.execute("SELECT * FROM packages WHERE adressee LIKE ?", ('%' + var + '%',))

    def populate_table(self, name=None, box=None, track=None):
        query="SELECT * FROM packages WHERE 1=1"
        if name:
            query += " AND adressee LIKE ?"
        if track:
            query += " AND tracking_number LIKE ?"
        if box:
            query += " AND box_number LIKE ?"
        results = self.cursor.execute(query, ('%' + name + '%',))
        return results.fetchall()

    def get_cadet_info(self, box):
        name = self.cursor.execute("SELECT name FROM cadets WHERE box_number = ?", (box,))
        names=''.join(item for item in name.fetchone() if item.isalnum())
        email=self.cursor.execute("SELECT email FROM cadets WHERE box_number = ?", (box,))
        emails=email.fetchall()
        return names, emails

    def close_connection(self):
        self.conn.close()
