import socket
import tqdm
import os
from _thread import *

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class Main:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created sucessfully")
        self.port = 5678

        self.s.bind(("127.0.0.1", self.port))
        print("Socket binded to %s" %(self.port))

        self.s.listen(5)
        print("Socket is listening")

        self.c_socket, self.addr = self.s.accept()
        self.msg = self.c_socket.recv(1024)
        self.message1 = self.msg.decode()
        self.choice = self.message1

        if self.choice == "Download":
            self.send_file()
        elif self.choice == "Upload":
            self.file_recieve()


    def send_file(self):
        while True:
            msgfromclient = self.c_socket.recv(1024)
            message = msgfromclient.decode()
            acfilename = message
            print("Got a connection from %s" % str(self.addr))
            print(acfilename)
            filename = (f"C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Server\\{acfilename}")
            with open(filename, 'rb') as f:
                file_contents = f.read()
                self.c_socket.sendall(file_contents)
            f.close()
            break
        self.c_socket.close()

    def file_recieve(self):
        print("Got a connection from %s" % str(self.addr))
        recieved = self.c_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = recieved.split(SEPARATOR)
        filename = os.path.basename("test"+filename)
        filesize = int(filesize)
        progress = tqdm.tqdm(range(filesize), f"Recieving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        fil = socket.gethostname()
        name = (f"{fil}.txt")

        with open(f"C:\\Users\\rahul\\Downloads\\New folder\\third_sem_Python\\Final_Project\\CW2\\Server\\{name}", "wb") as f:
            while True:
                bytes_read = self.c_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

if __name__ == "__main__":
    Main()