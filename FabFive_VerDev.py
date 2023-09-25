# FabFive Software, Version: Development Code (DevC 0.2)
# The development version uses print statements and omits the LCD functionality for testing purposes
# Author: Ammar Mohammed
import time

# from RPLCD import RPLCD
# lcd = CharLCD(cols = 16, rows=2, pin_rs=37, pin_e=35, pins_data=(33,31, ))

# Global variables
loop = True
user_list = []


class CardUser:
    # Number stores card number of user
    # Is_admin (boolean) stores whether user is admin
    def __init__(self, number, is_admin=False):
        self.number = number
        self.is_admin = is_admin


# This function will display "start-up" screen for our device
def boot_up():
    # lcd.cursor_pos = (0, 0)
    # lcd.write_string(u"MACHINE ONE")
    print('MACHINE ONE')  # Dev code

    time.sleep(1)
    # lcd.cursor_pos = (1, 0)
    # lcd.write_string(u"Please scan card")
    print('Please scan card')  # Dev code

    time.sleep(1)


# Function - dectect_user: reads the card numbers in the file and adds it to user_list
def detect_user():
    user_file = open("fabList.txt", "r")
    temp_list = user_file.readlines()
    user_file.close()

    for user in temp_list:
        user = user.strip('\n')
        user_list.append(user)

    print(user_list)


# Function - add_user: opens a new file to add the card number
def add_user(new_user):
    button_a = False  # yes button
    button_b = False  # no button
    print('Call Admin!')  # Perhaps we can have machine beep, or send ping to website
    # If admin at station, request admin to scan admin card
    print('Add user to system?')

    if button_a:
        button_a = False
        print('Access granted!')
        user_file = open("fabList.txt", "a")
        user_file.write(new_user + ' ')

        print('Is user admin?')
        # Read button inputs again
        if button_a:
            user_file.write('ADMIN' + '\n')
        elif button_b:
            user_file.write('DEFAULT' + '\n')

        user_file.close()

    elif button_b:
        button_b = False
        print('Access denied!')


# This is the main loop that will run at launch
while loop:
    boot_up()  # display welcome message

    detect_user()  # load in current user list

    card_number = input()  # retrieve card number
    current_user = CardUser(card_number)  # add card number to class

    # lcd.cursor_pos = (0,0)
    if card_number == "stop":  # developer bypass functionality
        loop = False
        # lcd.clear()
        # lcd.write_string(u"SYSTEM OFF...")
        print('SYSTEM OFF...')  # Dev code
    elif current_user.number in user_list:  # if user is found in list, grant access
        loop = False
        print('Welcome back ' + current_user.number)
    else:  # if user is not in list, goto add_user method
        loop = False
        # lcd.clear()

        # lcd.write_string(u"Welcome ")
        # lcd.write_string(current_user.number)
        print('Welcome ' + current_user.number)  # Dev code
        add_user(current_user.number)

        time.sleep(5)
        # lcd.clear()
