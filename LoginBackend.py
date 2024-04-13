import customtkinter as ctk
import tkinter as tk
import bcrypt

class User:
    def __init__(self, uname, pword, database):
        self.username=uname
        self.password=self.encode_pass(pword)
        self.db=database

    def encode_pass(self, pword):
        bytes=pword.encode('utf-8')
        salt=bcrypt.gensalt()
        hashed_password=bcrypt.hashpw(bytes, salt)
        return hashed_password

    def check_pass(self, pword):
        bytes=pword.encode('utf-8')
        print(bytes)
        users=self.db.cursor.execute(f"SELECT username, hashed_password FROM accounts WHERE username LIKE '{self.username}'")
        users=self.db.cursor.fetchone()
        print(users)
        
        if users:
            pword_encode=users[1]
            print(f"Password Should Be: {pword_encode}")
            if bcrypt.checkpw(bytes, pword_encode):
                print("Login Successful")
                return 1
            else:
                print("Password Incorrect")
                print(f"Password Was: {bytes}")
                return -1
        else:
            print("Username not recognized")
            return -2

    def store_login(self, admin):  
        existsp=self.db.cursor.execute(f"SELECT username FROM accounts WHERE username='{self.username}'").fetchone()
        if existsp: 
            print("Account already exists")
        else:
            string="INSERT INTO accounts (username, hashed_password, admin) VALUES (?, ?, ?)"
            self.db.cursor.execute(string, (self.username, self.password, admin))
            print("Account Created")
            self.db.conn.commit()
            
    
        
        
