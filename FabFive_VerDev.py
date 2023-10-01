# FabFive Software, Version: Development Code (DevC 0.5)
"""
DevC 0.5 
Added:
- Machine Activation
- Variable timer: shorter or longer timer based on whether user is default or admin respectively
Debug:
- Fixed code in main loop where user index was falsely identified: 
  user_index = card_number.index(current_user.number) when it should have been user_index = card_numbers.index(current_user.number) 
- Readjusted admin identifier to be 0 and 1 instead of "True" and "False" to avoid 'Truthy' error. <- when reading from files and adding to list
- Adjusted code so that 'button2' option in admin mode for set user to default in "add user" sub-menu does not take user to "remove user" sub-menu.
- For developer mode, user can input 'y' and 'n' in place of 'button1' and 'button2' respectively.
"""
# Author: Ammar Mohammed
import time
import csv
import RPi.GPIO as GPIO

loop = True

button1 = 18
button2 = 16
machine_pin = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(machine_pin, GPIO.OUT)  # check if internal resistor needs to be used

card_numbers = []
are_admins = []

user_index = -1
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
    time.sleep(1)

    print('Please scan card')  # Dev code
    time.sleep(1)


# Function displays a menu in which admins can either add or remove users
def admin_menu():
    button_response = True
    print('1. Add user?')
    print('2. Remove user?')

    while button_response:
        time.sleep(1)

        dev_input = input()  # DEV CODE

        # Add user sub-menu
        # if GPIO.input(button1) == 0:
        if dev_input == "y":  # DEV CODE
            button_response = False
            button_response1 = True

            print('ADD USER')
            print('Please scan card')
            user_add = input()

            print('Set user as admin?')
            while button_response1:
                time.sleep(1)

                dev_input = input()  # DEV CODE

                # if GPIO.input(button1) == 0:
                if dev_input == "y":  # DEV CODE
                    button_response1 = False
                    print('User set to admin')
                    add_user(user_add, 1)

                # if GPIO.input(button2) == 0:
                elif dev_input == "n":  # DEV CODE
                    button_response1 = False
                    print('User set to default')
                    add_user(user_add, 0)
                    time.sleep(1)
                    # break

        # Remove user sub-menu
        # if GPIO.input(button2) == 0:
        elif dev_input == "n":  # DEV CODE
            button_response = False
            print('REMOVE USER')
            print('Please scan card')
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
    # if user already in user list
    else:
        print('user already in system')
        print('add process cancelled')


# Function removes selected user from the user list
def remove_user(user):
    # check if user is currently in list
    if user in card_numbers:
        temp_index = card_numbers.index(user)
        card_numbers.remove(user)
        are_admins.pop(temp_index)
        print('User removed')
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


# Function turns activates machine while displaying the amount of time left before machine deactivates
def timer(time_duration):
    GPIO.output(machine_pin, True)  # turn on machine
    while time_duration > 0:
        print(time_duration)
        # Timer escape feature
        if GPIO.input(button2) == 0:
            print('Exited timer')
            break
        time.sleep(1)
        time_duration -= 1
    GPIO.output(machine_pin, False)  # turn off machine
    print('Finished timer')


# This while loop is the main loop
while loop:
    card_numbers = []
    are_admins = []

    boot_up()

    card_number = input()  # DEV CODE
    current_user = CardUser(card_number)

    print('In main loop, number: ' + current_user.number)  # DEV CODE
    print('In main loop, is_admin: ' + str(current_user.is_admin))  # DEV CODE

    # Read list from file
    try:
        user_file = open("fablist.csv", "r")
        csv_reader = csv.reader(user_file)

        for line in csv_reader:
            card_numbers.append(line[0])
            are_admins.append(int(line[1]))  # must cast to int first, because it's str, which would cause truthy
            # for '0' instead of falsy for 0
        user_file.close()
        print(card_numbers)  # DEV CODE
        print(are_admins)  # DEV CODE

    except FileNotFoundError:
        print('FILE NOT FOUND')
        # user_file = open("fablist.csv", "a")
        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')

        print('Created file')

    # See if user is already in list
    # If user is default, accept, turn on machine and timer
    if current_user.number in card_numbers:
        print('User recognized')
        print('Welcome back')
        user_index = card_numbers.index(current_user.number)
        current_user.is_admin = are_admins[user_index]
        print('See if user in list main(), index: ' + str(user_index))  # DEV CODE
        print('See user is admin: ' + str(current_user.is_admin))  # DEV CODE

    # If user not recognized, deny access, just say "To get added call Admin"
    if user_index == -1:
        print('User not found')
        print('To join the system, call admin for assistance')
    # if user is found
    else:
        # If admin scans launch admin menu (function)
        if current_user.is_admin:
            print('Access admin menu or use machine?')
            button_response = True

            while button_response:
                time.sleep(1)
                dev_input = input()  # DEV CODE
                if dev_input == "y":  # DEV CODE
                    button_response = False
                    admin_menu()
                elif dev_input == "n":  # DEV CODE
                    button_response = False
                    print('should turn machine on now')

                    admin_timer = 60 * seconds_per_minute  # admin gets an hour of usage
                    timer(admin_timer)
        # else turn on machine and start timer
        else:
            default_timer = minutes * seconds_per_minute  # default user gets 5 minutes of usage
            timer(default_timer)
    GPIO.cleanup()
