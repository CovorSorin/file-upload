import socket                  
import sys

# reserve a port
port = 6000

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine adress
host = socket.gethostname()
print host

# bind to the port and wait for client connection
s.bind((host, port))            
s.listen(10)                     

print 'Server listening...'

while True:
    
    # establish connection with client
    conn, addr = s.accept()
    
    print 'Connected to ', addr

    data = conn.recv(2048)
    print('Server received', repr(data))

    # creates a file to store the data from the client
    filename = 'received.txt'
    f = open(filename,'wb')
    f.write(data)

    print('File was received.')
    f = open(filename,'r')
    
    # store words from file received
    words = []

    for line in f:
        line = line.split(' ')
        for i in range(0, len(line)):
            if line[i] != '\n':
                words.append(line[i])
    f.close()

    print words
    words.sort()
    
    # send the words in the sorted order
    output = ""
    for i in range(0, (len(words))):
        output = output + str(words[i]) + " "
        
    conn.send(str(output))
    conn.close()