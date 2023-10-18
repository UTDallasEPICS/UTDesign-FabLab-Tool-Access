# FabFive Software, Version: Development Code (DevC 0.7)
"""
DevC 0.7
Added:
- Placed console print commands before lcd print commands
- Updated timer code: default users have timer, admin users have unlimited time
- Added time_spent variable (for admin and defaults) to keep track of user session
- Added Session Usage variable to store card number, time spent, start and stop time
"""
# Author: Ammar Mohammed
import time
import csv
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

loop = True

button1 = 13
button2 = 11
machine_pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(machine_pin, GPIO.OUT)

lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD)

card_numbers = []
are_admins = []

minutes = 5
seconds_per_minute = 2  # DEV CODE temporary number


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

        # dev_input = input()  # DEV CODE

        # Add user sub-menu
        if GPIO.input(button1) == 0:
            # if dev_input == "y":  # DEV CODE
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
            lcd.write_string('Set user as')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('admin?')

            while button_response1:
                time.sleep(1)

                # dev_input = input()  # DEV CODE

                if GPIO.input(button1) == 0:
                    # if dev_input == "y":  # DEV CODE
                    button_response1 = False

                    print('Setting new user as admin...')
                    lcd.clear()
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Setting new user')
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string('as admin...')
                    time.sleep(1)

                    print('User set to admin')
                    add_user(user_add, 1)

                elif GPIO.input(button2) == 0:
                    # elif dev_input == "n":  # DEV CODE
                    button_response1 = False

                    print('Setting new user as default...')
                    lcd.clear()
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string('Setting new user')
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string('as default...')
                    time.sleep(1)

                    print('User set to default')
                    add_user(user_add, 0)
                    time.sleep(1)
                    # break

        # Remove user sub-menu
        elif GPIO.input(button2) == 0:
            # elif dev_input == "n":  # DEV CODE
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
            card_numbers.append(user)
            are_admins.append(is_admin)

        print('User added')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('New user added')
        time.sleep(2)
        lcd.clear()

    # if user already in user list
    else:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User already in ')
        lcd.cursor_pos = (1, 0)
        lcd.write_string('system!!!')
        time.sleep(3)

        print('user already in system')
        print('add process cancelled')
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
        temp_index = card_numbers.index(user)
        card_numbers.remove(user)
        are_admins.pop(temp_index)

        print('User removed')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User now removed')
        time.sleep(1)

        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')
            counter = 0
            while counter < len(card_numbers):
                print('Inside remove(), number: ' + str(card_numbers[counter]))  # DEV CODE
                print('Inside remove(): are_admins: ' + str(are_admins[counter]))  # DEV CODE
                csv_writer.writerow([card_numbers[counter]] + [str(are_admins[counter])])
                counter += 1
            print('File updated')
    # if user was not in the user list
    else:
        print('user not found in list')
        print('removal process cancelled')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User not in list!')
        scroll_text('removal process cancelled', 1)


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

    GPIO.output(machine_pin, False)  # turn off machine

    print('Finished timer')
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Timer finished!')
    time.sleep(1)
    lcd.clear()


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


# This while loop is the main loop
while loop:
    time.sleep(1)
    lcd.clear()
    user_index = -1
    card_numbers = []
    are_admins = []

    boot_up()

    card_number = input()  # DEV CODE
    lcd.clear()
    if card_number == "stop":  # DEV CODE
        loop = False
        break
    current_user = CardUser(card_number)

    # Read list from file
    try:
        user_file = open("fablist.csv", "r")
        csv_reader = csv.reader(user_file)

        for line in csv_reader:
            card_numbers.append(line[0])
            are_admins.append(int(line[1]))  # must cast to int first, because it's str, which would cause truthy
            # for '0' instead of falsy for 0
        user_file.close()
        print(card_numbers)  # Read out the card numbers in the file
        print(are_admins)  # Read out the admin status in the file

    except FileNotFoundError:
        print('FILE NOT FOUND')
        # user_file = open("fablist.csv", "a")
        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')

        print('Created file')

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

        user_index = card_numbers.index(current_user.number)
        current_user.is_admin = are_admins[user_index]

    # If user not recognized, deny access, just say "To get added call Admin"
    if user_index == -1:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('User not found')
        time.sleep(1)

        print('User not found')
        print('To join the system, call admin for assistance')
        scroll_text('To join the system, call admin for assistance', 1)
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
                # dev_input = input()  # DEV CODE
                # if dev_input == "y":  # DEV CODE
                if GPIO.input(button1) == 0:
                    lcd.clear()
                    button_response = False
                    admin_menu()
                # elif dev_input == "n":  # DEV CODE
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
