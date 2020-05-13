#!/usr/bin/env python3
import sys
import re                                                   #split multiple patterns
import os.path                                              #check file exist

#reset
#=======================================================================================
file_path = '../record.txt'                                 #difine file path

#function
#=======================================================================================
def divide():                                               #divide line function
    print('='*40)

def read_data(record):
    with open(file_path, 'r') as fh:
        data = fh.readlines()
    return record + data

def read_balance():                                         #read balance function and return float
    with open(file_path, 'r') as fh:
        balance_in_file = float(fh.readline())                #read first line in file
    return balance_in_file

def write_balance(balance):                                 #write balance at the first in the file
    try:
        content = []
        with open(file_path, 'r') as fh:                    #read the old file content
            content = fh.readlines()
    except FileNotFoundError:                               #for the new start
        pass
    finally:
        with open(file_path, 'w') as fh:                    #rewrite the file with new balance
            fh.write(str(balance)+'\n')
            fh.writelines(content[1:])                      #skip the old balance

def file_to_list():                                         #read file and save it in a list
    content = []
    with open(file_path, 'r') as fh:
        for line in fh.readlines():
            content.append(re.split(':|\n', line)[:-1])
    return content

def user_add(user_input):                                   #user input 'add'
    balance = read_balance()
    error_exist = False                                     #error exist flag
    user_input_comma = user_input.split(',')                #set list split by ','
    with open(file_path, 'a') as fh:                        #add new data in the file
        for i in user_input_comma:
            try:                                            #set try-except to skip the error data
                i = i.split()                               #set list split by ' '
                i[1] = float(i[1])
                balance += i[1]
                fh.write(str(i[0])+':'+str(i[1])+'\n')      #append user input to record file
            except IndexError:                              #if the format is wrong
                error_exist = True
                sys.stderr.write(f'Invalid format. Fail to add a record {i}.\n')
            except ValueError:                              #if i[1] is not integer
                error_exist = True
                sys.stderr.write(f'Invalid value for money. Fail to add a record {i}.\n')
    write_balance(balance)

    if error_exist == True:                                 #format remind
        sys.stderr.write('The format of a record should be like this: breakfast -50\n\n')
    else:
        print('Add Success\n')
        return True

def user_view():                                            #user input 'view'
    print("Here's your expense and income records:")
    print('{:<20}{:<20}'.format('Description', 'Amount'))
    divide()
    with open(file_path, 'r') as fh:
        balance = float(fh.readline())
        for line in fh.readlines():
            content = line.split(':')
            print(f'{content[0]:<20}{content[1]}', end='')
    divide()
    print(f'Now you have {balance} dollars.\n')
    return 0

def user_delete(user_input):                                #user input 'delete'
    lines = []
    del_record = []
    s = user_input.split()
    s[1] = str(float(s[1]))

    with open(file_path, 'r') as fh:
        balance = float(fh.readline())
        for line in fh.readlines():
            lines.append(re.split(':|\n', line)[:2])        #split ':' and '\n' patterns and append the split_list into lines

    if s in lines:                                          #check if value exist
        last_index = len(lines) - lines[::-1].index(s) - 1  #find the last exist value index
        s[1] = float(s[1])
        balance -= s[1]                                     #count balance
        del(lines[last_index])                              #delete value

        del_record.append(str(balance) + '\n')
        for i, j in lines:
            s_format = str(i) + ':' + str(j) + '\n'
            del_record.append(s_format)
        with open(file_path, 'w') as fh:
            fh.writelines(del_record)
    else:
        sys.stderr.write(f'There is no record with ({s[0]} {s[1]}). Fail to delete a record\n\n')
        return False
    print('Delete Success\n')  
    return True

def user_reset():                                           #user input 'reset'
    os.remove(file_path)
    print(f'{file_path} has been Removed')

def user_find(user_input):
    user_input = (user_input.replace(' ', '')).split(',')
    content = file_to_list()
    summary = 0.0
    index = 1
    print('   {:<20}{:<20}'.format('Description', 'Amount'))
    divide()
    for user_key in user_input:
        for key, value in content[1:]:
            if user_key == key:
                value = float(value)
                print(f'{index:<3}{key:<20}{value:<20}')
                summary += value
                index += 1
            else:
                pass
    divide()
    print(f'Summary is {summary} dollars.\n')
    return 0

#main code
#=======================================================================================
#initial account balance
record = []
if os.path.exists(file_path):                               #check if file exist
    record = read_data(record)
    print('Welcome back!\n')
else:                                                       #do not exist then create new
    balance = 0.0                                           #initial balance
    try:
        balance = float(input('How much money do you have? '))
    except ValueError:
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n\n')
    finally:
        write_balance(balance)

print(record)

while True:
    user_input = input('What do you want to do (add/view/delete/exit/reset/find)? ')
    if user_input == 'add':
        user_add(input())
    elif user_input == 'view':
        user_view()
    elif user_input == 'delete':
        try:
            user_delete(input())    
        except Exception:
            sys.stderr.write('Wrong format\n\n')
    elif user_input == 'exit':
        break
    elif user_input == 'reset':
        user_reset()
        break
    elif user_input == 'find':
        user_find(input())
    else:
        sys.stderr.write('Invalid command. Try again\n\n')

print('Bye\n')











