#!/usr/bin/env python3
import sys
import os.path                                              #check file exist

#reset
#=======================================================================================
file_path = '../record.txt'                                 #difine file path

#function
#=======================================================================================
def divide():                                               #divide line function
    print('='*40)

def clean_newline(line):
    new_line = line.split('\n')[0]
    return new_line

def initialize():
    if os.path.exists(file_path):                               #check if file exist
        with open(file_path, 'r') as fh:
            data = fh.readlines()
        data = list(map(clean_newline, data))
        print('Welcome back!\n')
        if len(data) != 1:
            return float(data[0]), data[1:]
        else:
            return float(data[0]), []
    else:
        initial_money = 0.0                                           #initial balance
        try:
            initial_money = float(input('How much money do you have? '))
        except ValueError:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n\n')
        finally:
            return initial_money, []

def user_add(data):                           #user input 'add'
    record = data
    user_input = input()
    error_exist = False                                     #error exist flag
    user_input_comma = user_input.split(',')                #set list split by ','
    for i in user_input_comma:
        try:                                            #set try-except to skip the error data
            i = i.split()                               #set list split by ' '
            change_initial_money(float(i[1]))
            record.append(f'{i[0]}:{float(i[1])}')      #append user input to record
        except IndexError:                              #if the format is wrong
            error_exist = True
            sys.stderr.write(f'Invalid format. Fail to add a record {i}.\n')
        except ValueError:                              #if i[1] is not integer
            error_exist = True
            sys.stderr.write(f'Invalid value for money. Fail to add a record {i}.\n')

    if error_exist == True:                                 #format remind
        sys.stderr.write('The format of a record should be like this: breakfast -50\n\n')
    else:
        print('Add Success\n')
    return record

def user_view(data):                                            #user input 'view'
    record = data
    balance = initial_money
    print("Here's your expense and income records:")
    print('{:<20}{:<20}'.format('Description', 'Amount'))
    divide()
    for line in record:
        content = line.split(':')
        print(f'{content[0]:<20}{content[1]}')
    divide()
    print(f'Now you have {balance} dollars.\n')
    return

def user_delete(data):                                #user input 'delete'
    try:
        record = data
        new_record = []
        user_input = input().split()
        user_input[1] = str(float(user_input[1]))
        lines = []
        count = 0
        for line in record:
            x = line.split(':')
            lines.append(x)
            if x == user_input:
                count += 1
        if count == 0:
            sys.stderr.write(f'There is no record with ({user_input[0]} {user_input[1]}). Fail to delete a record\n\n')
            return record
        else:
            if count == 1:
                lines.pop(lines.index(user_input))
            else:
                divide()
                count = 1
                for line in lines:
                    if line == user_input:
                        print(f'{count:<3}{line[0]:<20}{line[1]}')
                        count += 1
                divide()
                index = int(input('Which one do you want to delete? '))
                if index > count-1:
                    raise Exception
                new_line = []
                count = 1
                for line in lines:
                    if count == index and line == user_input:
                        count += 1
                        continue
                    if line == user_input:
                        count += 1
                    new_line.append(line)
                lines = new_line

        for i in lines:
            new_record.append(f'{i[0]}:{i[1]}')
        print('Delete Success\n')
        change_initial_money(-(float(user_input[1])))
        return new_record
    except Exception:
            sys.stderr.write('Wrong format\n\n')
            return data

def user_reset():                                           #user input 'reset'
    os.remove(file_path)
    print(f'{file_path} has been Removed')

def user_find(record):
    pass

def user_save(balance, record):
    try:
        with open(file_path, 'w') as fh:
            fh.write(str(balance) + '\n')
            for line in record:
                fh.write(line + '\n')
        print('Finish Saving')
    except:
        sys.stderr.write('Fail To Save\n')

def change_initial_money(change):
    global initial_money 
    initial_money += change
    return

#main code
#=======================================================================================
#initial account balance
initial_money, record = initialize()
while True:
    user_input = input('What do you want to do (add/view/delete/exit/reset/find)? ')
    if user_input == 'add':
        record = user_add(record)
    elif user_input == 'view':
        user_view(record)
    elif user_input == 'delete':
        record = user_delete(record)    
    elif user_input == 'exit':
        user_save(initial_money, record)
        break
    elif user_input == 'reset':
        user_reset()
        break
    elif user_input == 'find':
        user_find(record)
    else:
        sys.stderr.write('Invalid command. Try again\n\n')

print('Bye\n')











