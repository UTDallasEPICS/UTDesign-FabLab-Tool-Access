# FabFive Software, Version: Developement Code
# The development version uses print statements and omits the LCD functionality for testing purposes
# Author: Ammar Mohammed
import time

# from RPLCD import RPLCD
# lcd = CharLCD(cols = 16, rows=2, pin_rs=37, pin_e=35, pins_data=(33,31, ))

# Global variables
card_number = ""
loop = True
login = False
user_list = []


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


# Function - add_user: opens a new file to add the card number
def add_user(new_user):
    user_file = open("fabList.txt", "a")
    user_file.write(new_user + '\n')
    user_file.close()


# Function - dectect_user: reads the card numbers in the file and adds it to user_list
def detect_user():
    user_file = open("fabList.txt", "r")
    temp_list = user_file.readlines()
    user_file.close()

    for user in temp_list:
        user = user.strip('\n')
        user_list.append(user)

    print(user_list)


# This is the main loop that will run at launch
while loop:
    boot_up()

    detect_user()

    card_number = input()

    # lcd.cursor_pos = (0,0)
    if card_number == "stop":
        loop = False
        # lcd.clear()
        # lcd.write_string(u"SYSTEM OFF...")
        print('SYSTEM OFF...')  # Dev code
    elif card_number in user_list:
        loop = False
        print('Welcome back ' + card_number)
    else:
        loop = False
        # lcd.clear()

        # lcd.write_string(u"Welcome ")
        # lcd.write_string(card_number)
        print('Welcome ' + card_number)  # Dev code
        add_user(card_number)

        time.sleep(5)
        # lcd.clear()

    '''
    elif card_number == "":
        lcd.clear()
        lcd.write_string(u"BLANK ERROR...")
        time.sleep(3)
    '''
