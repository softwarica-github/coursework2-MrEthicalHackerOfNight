from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter as tk
import socket
import tqdm
import customtkinter
import mysql.connector as mysql
from mysql.connector import Error
import csv
import hashlib
import subprocess

class Main:
    def __init__(self):
        self.root=Tk()
        self.root.title("File Transfer Software")
        self.root.geometry('500x600+500+100')
        self.root.minsize(400,200)
        self.root.maxsize(400,200)
        self.root.configure(bg='Sky blue')

        self.f1=font.Font(family='Serif',size='30')
        self.f2=font.Font(family='Serif',size='10')
        self.f3=font.Font(family='Serif',size='20')
        self.pic = PhotoImage(file='C:\\Users\\rahul\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\cover.png')

        self.p1 = Label(self.root, image=self.pic)
        self.p1.pack()

        
        self.convert=customtkinter.CTkButton(master=self.root,
                                 command=self.compl_server,
                                 text='Connect to Server',
                                 fg_color=("dodger blue", "dodger blue"))
        self.convert.place(relx='0.3',rely='0.7')

        self.root.mainloop()
    
    def compl_server(self):
        self.run_server()
        self.server_connect()

    def run_server(self):
        subprocess.Popen(["python", "C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Filesocket.py"])


    def server_connect(self):
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096

        self.s = socket.socket()
        self.port = 5678
        try:
            self.s.connect(('127.0.0.1', self.port))
            self.login_window()
        except:
            messagebox.showinfo('Info', "Servers are currently busy. Please try again later.")

    def login_window(self):
        self.root2 = Toplevel()
        self.root2.title("Login")
        self.root2.geometry("400x200")
        self.root2.minsize(400, 200)
        self.root2.maxsize(400, 200)

        self.p2 = Label(self.root2, image=self.pic)
        self.p2.pack()

        self.l3 = Label(self.root2, text="Username: ", font=("Serif", 10, "bold"))
        self.l3.place(relx='0.13', rely='0.2')
        self.l4 = Label(self.root2, text="Password: ", font=("Serif", 10, "bold"))
        self.l4.place(relx='0.13', rely='0.4')
        self.e1 = Entry(self.root2)
        self.e1.place(relx='0.45', rely='0.2', height='27')
        self.e2 = Entry(self.root2, show='*')
        self.e2.place(relx='0.45', rely='0.4', height='27')
        self.b1 = customtkinter.CTkButton(master=self.root2,
                                 command=self.login_db,
                                 text='Submit',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b1.place(relx='0.11', rely='0.65')

        self.b2 = customtkinter.CTkButton(master=self.root2,
                                 command=self.root.quit,
                                 text='Quit',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b2.place(relx='0.51', rely='0.65')

        self.b3 = customtkinter.CTkButton(master=self.root2, command=self.register_window,
                                 text='Register',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b3.place(relx='0.31', rely='0.8')


    def register_window(self): 
        self.root7 = Tk()
        self.root7.title("Register Account")
        self.root7.geometry("1000x800+250+0")
        self.root7.minsize(400, 500)
        self.root7.maxsize(400, 500)

        self.l6 = Label(self.root7, text="Register", fg='Black', font=("Serif", 25))
        self.l6.place(relx='0.5', rely='0.1', anchor='center')

        self.l7 = Label(self.root7, text=" First Name: ", fg='Black', font=("Serif", 10))
        self.l8 = Label(self.root7, text="Last Name: ", fg='Black', font=("Serif", 10))
        self.l9 = Label(self.root7, text="Username:", fg='Black', font=("Serif", 10))
        self.l10 = Label(self.root7, text="Password:", fg='Black', font=("Serif", 10))

        self.l7.place(relx='0.10', rely='0.25')
        self.l8.place(relx='0.10', rely='0.3')
        self.l9.place(relx='0.10', rely='0.35')
        self.l10.place(relx='0.10', rely='0.4')

        self.e7 = ttk.Entry(self.root7)
        self.e7.place(relx='0.40', rely='0.25', relwidth='0.45')
        self.e8 = ttk.Entry(self.root7)
        self.e8.place(relx='0.40', rely='0.30', relwidth='0.45')
        self.e9 = ttk.Entry(self.root7)
        self.e9.place(relx='0.40', rely='0.35', relwidth='0.45')
        self.e10 = ttk.Entry(self.root7)
        self.e10.place(relx='0.40', rely='0.40', relwidth='0.45')


        b = customtkinter.CTkButton(master=self.root7, command=self.register_db,
                                 text='Register',
                                 fg_color=("dodger blue", "dodger blue"))
        b.place(relx='0.31', rely='0.7')

    def login_db(self):
        self.database()
        #Error handling while connecting to the database
        try:
            conn = mysql.connect(host="localhost", user="root", password="", database="db_filetransfer")
            if conn.is_connected():
                cursor = conn.cursor()

        except Error as e:
            messagebox.showinfo('Info', "Host not found.")

        #Checking input field if it empty with prompt message
        if self.e1.get() == "" and self.e2.get() == "":
            messagebox.showinfo('Info', "Input field cant be blank.")

        #Storing user inputs in variable and matching values with table member from  database db_member.
        else:
            username = self.e1.get()
            password = self.e2.get()
            enc_password = hashlib.md5(f"{password}".encode('utf-8')).hexdigest()

            cursor.execute(f"SELECT username, password FROM db_users WHERE username = '{username}' AND password = '{enc_password}'")
            self.result = cursor.fetchone()
                    
            if self.result is None:
                messagebox.showinfo("Warning", "Invalid Username/Password.Please try again.")
            else:
                self.choice_window()
                
    def register_db(self):
        self.database()
        self.db_conn()

        self.FIRSTNAME = self.e7.get()
        self.LASTNAME = self.e8.get()
        self.USERNAME = self.e9.get()
        self.PASSWORD = self.e10.get()

        self.conn = mysql.connect(host="localhost",user="root",password="",database="db_filetransfer")

        if self.conn.is_connected():
            self.cursor = self.conn.cursor()      
            query = "INSERT INTO db_users(firstname, lastname, username, password) VALUES(%s, %s, %s, MD5(%s))"
            self.cursor.execute(query,(self.FIRSTNAME, self.LASTNAME, self.USERNAME, self.PASSWORD))
            self.conn.commit()
            messagebox.showinfo("Registration Succesfull")
            self.cursor.close()
            self.conn.close()
            self.user_store()

    def user_store(self):
        with open('C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.FIRSTNAME, self.LASTNAME, self.USERNAME, self.PASSWORD])

    def db_conn(self):
        # self.database()
        try:
            self.conn = mysql.connect(host="localhost",user="root",password="",database="db_filetransfer")
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.conn.close()
        except Error as e:
            pass

    def Table(self):
        self.db_conn()
       
        self.cursor.execute("DROP TABLE IF EXISTS db_users;")

        self.cursor.execute("CREATE TABLE db_users(firstname varchar(255),lastname varchar(255),username varchar(255),password varchar(255))")

        self.conn.commit()
        messagebox.showinfo("Table exists")

    def database(self):
        self.conn = mysql.connect(host="localhost",user="root",password="")
        if self.conn.is_connected():
            self.cursor =self.conn.cursor()
            try:
                self.cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'db_users')")
                self.cursor.execute(f"CREATE DATABASE db_filetransfer")
                self.conn.commit()
                # print("database created")
                self.cursor.close()
                self.conn.close()

            except Error as e:
                pass
                self.conn.close()  

    def choice_window(self):
        self.root3 = Toplevel()
        self.root3.title("Welcome to File Transfer.")
        self.root3.geometry("400x200")
        self.root3.minsize(400, 200)
        self.root3.maxsize(400, 200)

        self.p3 = Label(self.root3, image=self.pic)
        self.p3.pack()

        self.b4 = customtkinter.CTkButton(master=self.root3,
                                 command=self.upload_window,
                                 text='Upload',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b4.place(relx='0.21', rely='0.7')

        self.b5 = customtkinter.CTkButton(master=self.root3,
                                 command=self.download_window,
                                 text='Download',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b5.place(relx='0.61', rely='0.7')

        self.root2.destroy()
        self.root3.mainloop()

    def upload_window(self):
        self.root4 = Toplevel()
        self.root4.title("Please Select the file to upload")
        self.root4.geometry("400x200")
        self.root4.minsize(400, 200)
        self.root4.maxsize(400, 200)

        self.p4 = Label(self.root4, image=self.pic)
        self.p4.pack()

        self.b6 = customtkinter.CTkButton(master=self.root4,
                                 command=self.file_browse,
                                 text='Browse',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b6.place(relx='0.3', rely='0.7')
        
        self.root3.destroy()
        self.root4.mainloop()

    def file_browse(self):
        self.file = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
        self.s.sendall(b'Upload')
        if self.file:
            filename= (f"{self.file.name}")
            self.file.close()
        filesize = os.path.getsize(filename)
        self.s.send(f"{filename}<SEPARATOR>{filesize}".encode('UTF-8'))

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename,"rb") as f:
            while True:
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                self.s.sendall(bytes_read)
                progress.update(len(bytes_read))
                popup1 = 'File Upload Sucessfully.'
                messagebox.showinfo('Sucess', popup1)

    def download_window(self):
        self.root5 = Toplevel()
        self.root5.title("Select the file you want to download")
        self.root5.geometry("400x200")
        self.root5.minsize(400, 200)
        self.root5.maxsize(400, 200)

        self.flist = os.listdir("C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Server")
        
        self.lbox = tk.Listbox(self.root5)
        self.lbox.pack(padx=5,pady=10,fill=BOTH, expand=True)
        
        for item in self.flist:
            self.lbox.insert(tk.END, item)

        self.b7 = customtkinter.CTkButton(master=self.root5,
                                 command=self.showcontent,
                                 text='Download',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b7.place(relx='0.65', rely='0.85')

        self.root3.destroy()
        self.root5.mainloop()

    def entry_pop(self):
        self.root6 = Toplevel()
        self.root6.title('Name')
        self.root6.geometry("300x150")
        self.root6.minsize(300, 200)
        self.root6.maxsize(300, 200)

        self.p6 = Label(self.root6, image=self.pic)
        self.p6.pack()

        self.l6 = Label(self.root6, text="Give name for file", font=("Serif", 10))
        self.l6.place(relx='0.33', rely='0.2')
        self.t6 = Text(self.root6, height=1, width=30)
        self.t6.place(relx='0.1', rely='0.4')

        self.b8 = customtkinter.CTkButton(master=self.root6,
                                 command=self.recieve_file,
                                 text='Ok',
                                 fg_color=("dodger blue", "dodger blue"))
        self.b8.place(relx='0.33', rely='0.7')

    def recieve_file(self):
        received = bytearray()
        while True:
            data = self.s.recv(4096)
            if not data:
                break
            received.extend(data)
            rec_name = self.t6.get("1.0", "end-1c")
            with open(f"C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Client\\{rec_name}.txt", 'wb') as f:
                f.write(received)
            f.close()
            popup2 = 'File Download Sucessfully'
            messagebox.showinfo('Sucess', popup2)
            break
        self.s.close()

    def showcontent(self):
        self.s.sendall(b'Download')
        x = self.lbox.curselection()[0]
        file = self.lbox.get(x)
        print(file)
        with open(f"C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Server\\{file}"):
            filename = file
            self.s.sendall(filename.encode('UTF-8'))
            self.entry_pop()

if __name__ == "__main__":
    Main()