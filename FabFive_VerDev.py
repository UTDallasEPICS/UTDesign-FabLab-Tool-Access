# FabFive Software, Version: Development Code (DevC 0.3)
# DevC 0.3 Button Input Functionality Added
# Author: Ammar Mohammed
import time
import RPi.GPIO as GPIO
from RPLCD import CharLCD

# Setup Button Pins
GPIO.setmode(GPIO.BOARD)
button1 = 18  # yes button
button2 = 16  # no button
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#BUG AT THIS LINE, when ever this line is uncommented,
#it somehow makes the program think button1 at pin 18 is pressed
#lcd = CharLCD(cols = 16, rows=2, pin_rs=37, pin_e=35, pins_data=(33,31, 29, 23), numbering_mode=GPIO.BOARD)

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
    #lcd.cursor_pos = (0, 0)
    #lcd.write_string(u"MACHINE ONE")
    print('MACHINE ONE')  # Dev code

    time.sleep(1)
    #lcd.cursor_pos = (1, 0)
    #lcd.write_string(u"Please scan card")
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
    admin_mode = True  # var for while loop to wait for button response
    user_create_process = False
    
    print('Call Admin!')  # Perhaps we can have machine beep, or send ping to website
    # If admin at station, request admin to scan admin card
    print('Add user to system?')
    
    while admin_mode:
        time.sleep(.3)
        print('Yes Button: ' + str(GPIO.input(button1)))
        print('No Button: ' + str(GPIO.input(button2)))
        if GPIO.input(button1) == 0:  # 0 means pressed
            admin_mode = False
            print('Access granted!')
            user_file = open("fabList.txt", "a")
            user_file.write(new_user + ' ')
            user_file.close()
            print('User added')
            user_create_process = True

        elif GPIO.input(button2) == 0:
            admin_mode = False
            print('Access denied!')
    
    if user_create_process:
        print('Is user admin?')
    while user_create_process:
        time.sleep(.5)
        # Read button inputs again
        if GPIO.input(button1) == 0:
            user_file = open("fabList.txt", "a")
            user_file.write('ADMIN' + '\n')
            user_file.close()
	    print('user set to admin')
	    user_create_process = False
        elif GPIO.input(button2) == 0:
            user_file = open("fabList.txt", "a")
            user_file.write('DEFAULT' + '\n')
            user_file.close()
	    print('user set to default')
	    user_create_process = False
              
# This is the main loop that will run at launch
while loop:
    boot_up()  # display welcome message

    card_number = raw_input()  # retrieve card number
    current_user = CardUser(card_number)  # add card number to class
    
    try:
        detect_user()  # load in current user list
        print('users detected')
    except:
        print('File Does NOT Exist!')
    finally:
        print('process complete')

    #lcd.cursor_pos = (0,0)
    if card_number == "stop":  # developer bypass functionality
        loop = False
        #lcd.clear()
        #lcd.write_string(u"SYSTEM OFF...")
        print('SYSTEM OFF...')  # Dev code
    elif current_user.number in user_list:  # if user is found in list, grant access
        loop = False
        print('Welcome back ' + current_user.number)
    else:  # if user is not in list, goto add_user method
        loop = False
        #lcd.clear()

        #lcd.write_string(u"Welcome ")
        #lcd.write_string(current_user.number)
        print('Welcome ' + current_user.number)  # Dev code
        add_user(current_user.number)

        time.sleep(5)
        #lcd.clear()
