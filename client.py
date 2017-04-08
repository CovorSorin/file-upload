import socket                   
import sys

# get local machine adress
port = 6000

# reserve a port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create a socket object
host = socket.gethostname()
host = '192.168.0.100'

# connect to the host
s.connect((host, port))

f = open('file.txt', 'rb')

print 'The file is sending...'

for line in f:
    s.send(line)
        
f.close()

print('File succesfully sent!')

words = ''
# wait for response
while True:
    data = s.recv(1024)
    words = words + str(data) + ' '
    if not data:
        break

print(words)
s.close()
print('Connection closed.')
