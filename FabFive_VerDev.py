# FabFive Software, Version: Development Code (DevC 0.4)
# DevC 0.4 Changes according to new plan: DesignModel2023Sept28. Switched to csv file format.
# Author: Ammar Mohammed
import time
import csv
import RPi.GPIO as GPIO

loop = True

button1 = 16
button2 = 18
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

card_numbers = []
are_admins = []

user_index = -1
minutes = 5
time_duration = minutes * 60


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


def admin_menu():
    button_response = True
    print('1. Add user?')
    print('2. Remove user?')

    while button_response:
        # Add user sub-menu
        if GPIO.input(button1) == 0:
            button_response = False
            button_response1 = True

            print('ADD USER')
            print('Please scan card')
            user_add = input()

            print('Set user as admin?')
            while button_response1:
                time.sleep(0.5)
                if GPIO.input(button1) == 0:
                    button_response1 = False
                    print('User set to admin')
                    add_user(user_add, True)

                if GPIO.input(button2) == 0:
                    button_response1 = False
                    print('User set to default')
                    add_user(user_add, False)

        # Remove user sub-menu
        if GPIO.input(button2) == 0:
            button_response = False
            print('REMOVE USER')
            print('Please scan card')
            user_remove = input()
            remove_user(user_remove)


        time.sleep(0.5)


# check is user already in system
def add_user(user, is_admin):
    if user not in card_numbers:
        with open("fablist.csv", "a") as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow([user] + [str(is_admin)])
            card_numbers.append(user)
            are_admins.append(is_admin)
        print('User added')


def remove_user(user):
    if user in card_numbers:
        temp_index = card_numbers.index(user)
        card_numbers.remove(user)
        are_admins.pop(temp_index)
        print('User removed')
        with open("fablist.csv", "w") as user_file:
            csv_writer = csv.writer(user_file, delimiter=',')
            counter = 0
            while counter < len(card_numbers):
                csv_writer.writerow([card_numbers[counter]] + [str(are_admins[counter])])
                counter += 1
        print('File updated')


while loop:
    boot_up()

    card_number = input()  # DEV CODE
    current_user = CardUser(card_number)

    # Read list from file
    try:
        user_file = open("fablist.csv", "r")
        csv_reader = csv.reader(user_file)

        for line in csv_reader:
            card_numbers.append(line[0])
            are_admins.append(bool(line[1]))

        user_file.close()
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
        user_index = card_number.index(current_user.number)
        current_user.is_admin = are_admins[user_index]

    # If user not recognized, deny access, just say "To get added call Admin"
    if user_index == -1:
        print('User not found')
        print('To join the system, call admin for assistance')
    # if user is found
    else:
        # If admin scans launch admin menu (function)
        if current_user.is_admin:
            admin_menu()
        # else turn on machine and start timer
        else:
            while time_duration > 0:
                print(time_duration)
                # Timer escape feature
                if GPIO.input(button2) == 0:
                    print('Exited timer')
                    break
                time.sleep(1)
                time_duration -= 1
            print('Finished timer')
