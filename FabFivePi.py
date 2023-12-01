# FabFive Software, Version: FabFivePi V9
"""
FabFivePi V9.0
- Removed socket server connection
- Fixed lcd.cursor_pos to follow row, column format: made mistake of col, row
"""
# Author: Ammar Mohammed
import time
import csv
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import json
import mysql.connector

loop = True

'''Pin declarations'''
button1 = 13
button2 = 11
machine_pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(machine_pin, GPIO.OUT)

lcd = CharLCD('PCF8574', 0x27)

card_numbers = {}

minutes = 5
seconds_per_minute = 60  # DEV CODE temporary number


class CardUser:
    # Number stores card number of user
    # Is_admin (boolean) stores whether user is admin
    def __init__(self, number, is_admin=False):
        self.number = number
        self.is_admin = is_admin


# This function will display "start-up" screen for our device
def boot_up():
    print('MACHINE ONE')  # Dev code
    lcd.cursor_pos = (0, 0)
    lcd.write_string('MACHINE ONE')
    time.sleep(1)

    print('Please scan card')  # Dev code
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Please scan card')
    time.sleep(1)


# Function displays a menu in which admins can either add or remove users
def admin_menu():
    button_response = True

    print('1. Add user?')
    print('2. Remove user?')
    lcd.cursor_pos = (0, 0)
    lcd.write_string('1. Add user?')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('2. Remove user?')

    while button_response:
        time.sleep(1)

        # Add user sub-menu
        if GPIO.input(button1) == 0:
            button_response = False
            button_response1 = True

            lcd.clear()

            print('ADD USER')
            print('Please scan card')
            lcd.cursor_pos = (0, 0)
            lcd.write_string('ADD USER')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('Scan card to add')

            user_add = input()

            print('Set user as admin?')
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('Set user as admin?')
            lcd.cursor_pos = (2, 0)
            lcd.write_string('Button 1: YES')
            lcd.cursor_pos = (3, 0)
            lcd.write_string('Button 2: NO')

            while button_response1:
                time.sleep(1)
                if GPIO.input(button1) == 0:
                    button_response1 = False

                    print('Setting new user as admin...')
                    lcd.clear()
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Setting new user')
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string('as admin...')
                    time.sleep(1)

                    add_user(user_add, 1)

                elif GPIO.input(button2) == 0:
                    button_response1 = False

                    print('Setting new user as default...')
                    lcd.clear()
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Setting new user')
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string('as default...')
                    time.sleep(1)

                    add_user(user_add, 0)
                    time.sleep(1)

        # Remove user sub-menu
        elif GPIO.input(button2) == 0:
            button_response = False

            print('REMOVE USER')
            print('Please scan card')
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('REMOVE USER')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('Please scan card')

            user_remove = input()
            remove_user(user_remove)


# Function adds users if they are not found in user list and sets new user to either admin or default
def add_user(user, is_admin):
    # if user not found in user list
    if user not in card_numbers:
        with open("fablist.csv", "a") as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow([user] + [is_admin])
            card_numbers.update({user: is_admin})

        print({True: 'User set to admin!', False: 'User set to default!'}[is_admin])
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('New user added')
        time.sleep(2)
        lcd.clear()

    # if user already in user list
    else:
        print('User already in system')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User already in')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('system!!!')
        time.sleep(3)

        print('Add process cancelled')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('Add user process')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('cancelled!!!')
        time.sleep(3)


# Function removes selected user from the user list
def remove_user(user):
    # check if user is currently in list
    if user in card_numbers:
        card_numbers.pop(user)

        print('User removed')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User now removed')
        time.sleep(1)

        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')

            for dict_number, dict_admin in card_numbers.items():
                csv_writer.writerow([dict_number] + [str(dict_admin)])  # important to put [] so commas appear correctly
            print('File updated')
    # if user was not in the user list
    else:
        print('user not found in list')
        print('removal process cancelled')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User not in list!')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('removal process')
        lcd.cursor_pos = (2, 0)
        lcd.write_string('cancelled')


# Function turns activates machine while displaying the amount of time left before machine deactivates
def timer(user_type):
    GPIO.output(machine_pin, True)  # turn on machine
    time.sleep(1)  # buffer button2 input

    get_time = time.localtime()
    start_time = time.strftime("%H:%M:%S", get_time)
    print(start_time)

    if user_type == 'default':
        default_timer = minutes * seconds_per_minute
        default_time_spent = 0
        while default_timer > 0:
            print(default_timer)
            lcd.cursor_pos = (0, 0)
            lcd.write_string('Seconds: ' + str(default_timer))
            lcd.cursor_pos = (1, 0)
            lcd.write_string('Exit: Button 2')

            # Timer escape feature
            if GPIO.input(button2) == 0:
                print('Exited timer')
                lcd.cursor_pos = (0, 0)
                lcd.write_string('EXIT TIMER...')
                time.sleep(1)
                break
            time.sleep(1)
            default_timer -= 1
            default_time_spent += 1
            lcd.clear()
        print('Total time spent: ' + str(default_time_spent))

        get_time = time.localtime()
        stop_time = time.strftime("%H:%M:%S", get_time)
        print(stop_time)

        session_usage = f'{current_user.number}, {default_time_spent}, {start_time}, {stop_time}'  # stores data of how long user used machine
        print(session_usage)
        session_data = json.dumps(session_usage)
        # send_data(session_data)

    elif user_type == 'admin':
        admin_time_spent = 0
        admin_use_machine = True

        while admin_use_machine:
            print(admin_time_spent)
            lcd.cursor_pos = (0, 0)
            lcd.write_string('Time (s): ' + str(admin_time_spent))
            lcd.cursor_pos = (1, 0)
            lcd.write_string('Exit: Button 2')

            # Timer escape feature
            if GPIO.input(button2) == 0:
                admin_use_machine = False
                print('Exited timer')
                lcd.cursor_pos = (0, 0)
                lcd.write_string('EXIT TIMER...')
                time.sleep(1)
                break
            time.sleep(1)
            admin_time_spent += 1
            lcd.clear()
        print('Total time spent: ' + str(admin_time_spent))

        get_time = time.localtime()
        stop_time = time.strftime("%H:%M:%S", get_time)
        print(stop_time)

        session_usage = f'{current_user.number}, {admin_time_spent}, {start_time}, {stop_time}'  # stores data of how long user used machine
        print(session_usage)
        session_data = json.dumps(session_usage)
        # send_data(session_data)

    GPIO.output(machine_pin, False)  # turn off machine

    print('Finished timer')
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Timer finished!')
    time.sleep(1)
    lcd.clear()


'''Developed for 16x2 LCD
Starts printing string at last digit panel on screen,
then carries the text forward
'''


def scroll_text(long_text, line_number):
    length_text = len(long_text)
    for i in range(length_text):
        if (15 - i) > -1:
            lcd.cursor_pos = (line_number, (15 - i))
            lcd.write_string(long_text)
        else:
            lcd.cursor_pos = (line_number, 0)
            lcd.write_string(long_text[abs(15 - i):length_text])
        time.sleep(0.25)
    time.sleep(1)
    lcd.clear()


# def send_data(data):
#     print(data)
#
#     print('Connecting to server...')
#     lcd.clear()
#     lcd.cursor_pos = (0, 0)
#     lcd.write_string('Connecting to')
#     lcd.cursor_pos = (1, 0)
#     lcd.write_string('server...')
#     time.sleep(1)
#
#     bytes_to_send = data.encode('utf-8')
#     server_address = ('192.168.254.209', 2222)
#     buffer_size = 1024
#     udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_client.settimeout(20)  # testing 20 second unresponsive
#     try:
#         udp_client.sendto(bytes_to_send, server_address)
#
#         response, address = udp_client.recvfrom(buffer_size)
#         response = response.decode('utf-8')
#         print('Response from Server', response)
#         print('Server IP Address: ', address[0])
#         print('Server Port: ', address[1])
#
#         lcd.clear()
#         lcd.cursor_pos = (0, 0)
#         lcd.write_string('Reached server!')
#         time.sleep(1)
#     except socket.timeout:
#         print('ERROR: Cannot reach server')
#         lcd.clear()
#         lcd.cursor_pos = (0, 0)
#         lcd.write_string('ERROR: Server')
#         lcd.cursor_pos = (1, 0)
#         lcd.write_string('unavailable')
#         time.sleep(5)


# mysql code
db = mysql.connector.connect(
    host="",
    user="FabFive",
    passwd="FabFive",
    database="Fablab"
)

# This while loop is the main loop
while loop:
    time.sleep(1)
    # Read list from file
    try:
        user_file = open("fablist.csv", "r")
        csv_reader = csv.reader(user_file)

        for line in csv_reader:
            card_numbers.update({line[0]: int(line[1])})
            # must cast to int first, because it's str, which would cause truthy
            # for '0' instead of falsy for 0
        user_file.close()

    # if file not found, create the card list file
    except FileNotFoundError:
        print('FILE NOT FOUND')
        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')

        print('Created file')

    card_data = json.dumps(card_numbers)  # converts list of card numbers to JSON
    # send_data(card_data)
    lcd.clear()

    boot_up()  # just prints text on screens

    card_number = input()  # DEV CODE
    lcd.clear()
    if card_number == "stop":  # DEV CODE
        loop = False
        break
    current_user = CardUser(card_number)

    # See if user is already in list
    # If user is default, accept, turn on machine and timer
    if current_user.number in card_numbers:
        lcd.cursor_pos = (0, 0)
        print('User recognized')
        lcd.write_string('User recognized')
        time.sleep(1)

        lcd.cursor_pos = (1, 0)
        print('Welcome back')
        lcd.write_string('Welcome back')
        time.sleep(2)
        lcd.clear()

        current_user.is_admin = card_numbers.get(current_user.number)

    # If user not recognized, deny access, just say "To get added call Admin"
    if current_user.number not in card_numbers.keys():
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        print('User not found')
        lcd.write_string('User not found')
        time.sleep(1)

        print('To join the system, call admin for assistance')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('To join the system,')
        lcd.cursor_pos = (2, 0)
        lcd.write_string('call admin for')
        lcd.cursor_pos = (3, 0)
        lcd.write_string('assistance')
    # if user is found
    else:
        # If admin scans launch admin menu (function)
        if current_user.is_admin:
            print('Access admin menu or use machine?')
            button_response = True

            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('1. Admin Menu')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('2. Use Machine')

            while button_response:
                time.sleep(1)
                if GPIO.input(button1) == 0:
                    lcd.clear()
                    button_response = False
                    admin_menu()
                elif GPIO.input(button2) == 0:
                    button_response = False
                    print('Starting Machine...')
                    lcd.clear()

                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Starting Machine')
                    time.sleep(1)
                    lcd.clear()

                    timer('admin')

        # else turn on machine and start timer
        else:
            print('Starting machine')
            lcd.cursor_pos = (0, 0)
            lcd.write_string('Starting Machine')
            time.sleep(1)
            lcd.clear()

            timer('default')
print('Cleaning GPIO pins')
lcd.clear()
GPIO.cleanup()
