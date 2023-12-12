import socket
import mysql.connector
bufferSize = 1024
ServerPort = 2222
ServerIP = '10.42.0.1'  # IP address of server Pi when connected to FabFive Wifi-Hotspot, password to hotspot, fabfive1

msgFromServer = "Thanks! Server received timelog data."
bytesToSend = msgFromServer.encode('utf-8')

RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((ServerIP, ServerPort))

print('Server is up and listening...')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="fablab"
)
my_cursor = db.cursor()

#'''
while True:
    logdata, address = RPIsocket.recvfrom(bufferSize)
    logdata = logdata.decode('utf-8')
    print(logdata)
    print('Client Address: ', address[0])
    RPIsocket.sendto(bytesToSend, address)
    mysql_command = f'INSERT INTO timelog(userID, adminStatus, machineType, date, startTime, endTime) VALUES({logdata})'
    my_cursor.execute(mysql_command)
    db.commit()
    if logdata == 'shutdown':
        break
#'''
