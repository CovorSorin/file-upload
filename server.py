import socket                  

# reserve a port
port = 6000

# create a socket object
s = socket.socket()

# get local machine adress
host = socket.gethostname()     

# bind to the port and wait for client connection
s.bind((host, port))            
s.listen(10)                     

print 'Server listening...'

while True:
    
    # establish connection with client
    conn, addr = s.accept()
    
    print 'Connected to ', addr

    data = conn.recv(1024)
    print('Server received', repr(data))

    # creates a file to store the data from the client
    filename = 'received.txt'
    f = open(filename,'wb')
    f.write(data)
    f.close()

    print('File was received.')

    # store words from file received
    words = []

    f = open(filename,'rb')
    for line in f:
        line = line.split()
        words.append(line)
    f.close()

    words.sort()
    
    # send the words in the sorted order
    output = ""
    for i in range(0, (len(words)-1)):
        output = output + str(words[i])
        
    conn.send(str(output))
    conn.close()

