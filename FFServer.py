import socket
bufferSize = 1024
ServerPort = 2222
ServerIP = '192.168.254.209'  # IP address of server, ifconfig

msgFromServer = "Thanks! Server received user-card list."
bytesToSend = msgFromServer.encode('utf-8')  # encode the message

# set up the socket/server
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((ServerIP, ServerPort))

# print after server is setup
print('Server is Up and Listening...')  # guy at counter waits for customer to order something

# information received from client
while True:
    message, address = RPIsocket.recvfrom(bufferSize)  # receive message and address of client connecting to server
    message = message.decode('utf-8')  # decode client message
    print(message)  # print message from client
    print('Client Address', address[0])  # print address of client
    RPIsocket.sendto(bytesToSend, address)
