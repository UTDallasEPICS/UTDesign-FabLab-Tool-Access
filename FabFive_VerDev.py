# FabFive Software, Version: Developement Code
# The development version uses print statements and omits the LCD functionality for testing purposes
# Author: Ammar Mohammed
import time

# from RPLCD import RPLCD
# lcd = CharLCD(cols = 16, rows=2, pin_rs=37, pin_e=35, pins_data=(33,31, ))

name = ""
loop = True
login = False
user_list = []


def boot_up():
    # lcd.cursor_pos = (0, 0)
    # lcd.write_string(u"MACHINE ONE")
    print('MACHINE ONE')  # Dev code

    time.sleep(1)
    # lcd.cursor_pos = (1, 0)
    # lcd.write_string(u"Please scan card")
    print('Please scan card')  # Dev code

    time.sleep(1)


def add_user(new_name):
    user_file = open("fabList.txt", "a")
    user_file.write(new_name + '\n')
    user_file.close()


def detect_user():
    user_file = open("fabList.txt", "r")
    temp_list = user_file.readlines()
    user_file.close()

    for user in temp_list:
        user = user.strip('\n')
        user_list.append(user)

    print(user_list)


while loop:
    boot_up()

    detect_user()

    name = input()

    # lcd.cursor_pos = (0,0)
    if name == "stop":
        loop = False
        # lcd.clear()
        # lcd.write_string(u"SYSTEM OFF...")
        print('SYSTEM OFF...')  # Dev code
    elif name in user_list:
        loop = False
        print('Welcome back ' + name)
    else:
        loop = False
        # lcd.clear()

        # lcd.write_string(u"Welcome ")
        # lcd.write_string(name)
        print('Welcome ' + name)  # Dev code
        add_user(name)

        time.sleep(5)
        # lcd.clear()

    '''
    elif name == "":
        lcd.clear()
        lcd.write_string(u"BLANK ERROR...")
        time.sleep(3)
    '''
