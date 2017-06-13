import socket
import sys
import Tkinter as tk
from Tkinter import *
import tkFont
import urllib2

root = tk.Tk()
root.title("ABC")

def sort():
    file_name = e.get()

    # file_name = urllib2.urlopen(url)
    
    # create a socket object
    port = 6000

    # reserve a port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine adress
    host = socket.gethostname()

    # connect to the host
    s.connect((host, port))

    # file_name = sys.argv[1]
    f = open(file_name, 'rb')

    print 'The file is sending...'

    for line in f:
        s.sendall(line)

    f.close()

    print('File succesfully sent!')

    result = ""
    
    # wait for response
    while True:
        data = s.recv(2048)
        result = result + str(data)
        if not data:
            break

    print result
    s.close()
    print('Connection closed.')
    w2.config(text = result)

helv = tkFont.Font(family = 'Helvetica', size = 16, weight = 'bold')

w1 = Label(root, text = "Type the name of the file that contains the words that you wish to sort:", font = helv)
w1.pack()

frame = Frame(root)
frame.pack()

e = Entry(root, bd = 5, font = helv, width = 60)
e.pack()

button = Button(root, text = "Sort", fg = "red", command = sort, font = helv)
button.pack()

w2 = Label(root, text = "The result will be placed here.", font = helv)
w2.pack()

root.geometry("1000x500")
root.mainloop()
