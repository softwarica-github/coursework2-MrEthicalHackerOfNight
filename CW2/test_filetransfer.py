import unittest
from filetransfer import Main
import socket
import mysql.connector as mysql
from mysql.connector import Error
from tkinter import filedialog
import hashlib

class TestFiletransfer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_send(self):
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096

        self.s = socket.socket()

        self.port2 = 1234

        self.s.connect(('127.0.0.1', self.port2))
        try:
            self.file = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
            self.s.sendall(b'Upload')
        except:
            self.fail("Server Down. Cannot send.")
        finally:
            self.s.close()

    def test_registration(self):
        self.firstName = "Ram"
        self.lastname = "Ramm"
        self.username = "unitest"
        self.password = "1234"

        self.conn2 = mysql.connect(host="localhost",user="root",password="",database="db_filetransfer")
        self.cursor2 = self.conn2.cursor()
        query2 = "INSERT INTO db_users(firstname, lastname, username, password) VALUES(%s, %s, %s, %s)"
        self.cursor2.execute(query2,(self.firstName, self.lastname, self.username, self.password))
        self.conn2.commit()

        self.cursor2.execute(f"SELECT username, password FROM db_users WHERE username = '{self.username}' AND password = '{self.password}'")
        self.result2 = self.cursor2.fetchone()
        if self.result2 != None:
            pass
        else:
             self.fail("Registration Failed.")

    def test_login(self):
        self.conn = mysql.connect(host="localhost",user="root",password="",database="db_filetransfer")
        self.cursor = self.conn.cursor()
        self.tusername = 'test'
        self.tpassword = hashlib.md5("test".encode('utf-8')).hexdigest()

        self.cursor.execute(f"SELECT username, password FROM db_users WHERE username = '{self.tusername}' AND password = '{self.tpassword}'")
        self.result = self.cursor.fetchone()

        if self.result != None:
            pass
        else:
             self.fail("Invalid Details")

    def test_database(self):
        try:
            self.conn = mysql.connect(host="localhost",user="root",password="",database="db_filetransfer")
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.conn.close()
        except ConnectionRefusedError:
            self.fail("Failed to connect to the database.")

if __name__ == '__main__':
    unittest.main()