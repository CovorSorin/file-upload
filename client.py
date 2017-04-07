import socket                   

# get local machine adress
port = 6000

# reserve a port
s = socket.socket()

# create a socket object
host = socket.gethostname()

# connect to the host
s.connect((host, port))

f = open('file.txt', 'rb')

print 'The file is sending...'

for line in f:
    s.send(line)
        
f.close()

print('File succesfully sent!')

while True:
    data = s.recv(1024)
    print('data=%s', (data))
    if not data:
        break
    
s.close()
print('Connection closed.')
