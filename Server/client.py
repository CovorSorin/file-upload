import socket
import sys

# create a socket object
port = 6000

# reserve a port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine adress
host = socket.gethostname()

# connect to the host
s.connect((host, port))

f = open('file.txt', 'rb')

print 'The file is sending...'

for line in f:
    s.sendall(line)
        
f.close()

print('File succesfully sent!')

words = ''
# wait for response
while True:
    data = s.recv(2048)
    words = words + str(data) + ' '
    if not data:
        break

print(words)
s.close()
print('Connection closed.')
