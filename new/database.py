import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.db_name=db_name
        print(f"Initialized connection to {self.db_name}")
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cadets (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       email TEXT,
                       graduation_date DATE,
                       box_number INTEGER);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS packages (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tracking_number INTEGER,
                       adressee TEXT,
                       received DATE,
                       picked_up DATE);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                            id INT PRIMARY KEY,
                            username STRING(100) UNIQUE,
                            hashed_password STRING(100),
                            admin INT);""")
                            

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
            query += f" AND adressee LIKE '%{name}%'"
        if track:
            query += f" AND tracking_number LIKE '%{track}%'"
        if box:
            query += f" AND box_number LIKE '%{box}%'"
        results = self.cursor.execute(query)
        results=results.fetchall()
        return results

    def close_connection(self):
        self.conn.close()
