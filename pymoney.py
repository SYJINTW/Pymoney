#!/usr/bin/env python3
import sys
import re
import os.path

#reset
#=======================================================================================
record = [['a',20],['a',30],['a',20],['a',20],['a',30]]
file_path = '../record.txt'



#function
#=======================================================================================
def divide():                                                   #divide line function
    print('='*40)

def read_balance():
    with open(file_path, 'r') as fh:
        balance_in_file = int(fh.readline())
    return balance_in_file

def write_balance(balance):
    try:
        content = []
        with open(file_path, 'r') as fh:
            content = fh.readlines()
    except FileNotFoundError:
        pass
    finally:
        with open(file_path, 'w') as fh:
            fh.write(str(balance)+'\n')
            fh.writelines(content[1:])

#user input 'add'
def user_add(user_input):
    balance = read_balance()                                             #set 'balance' in the func global
    error_exist = False
    user_input_comma = user_input.split(',')                    #set list split by ','
    with open(file_path, 'a') as fh:
        for i in user_input_comma:
            try:
                i = i.split()
                i[1] = int(i[1])
                balance += i[1]
                fh.write(str(i[0])+':'+str(i[1])+'\n')      #append user input to record file
            except IndexError:
                error_exist = True
                sys.stderr.write(f'Invalid format. Fail to add a record {i}.\n')
            except ValueError:
                error_exist = True
                sys.stderr.write(f'Invalid value for money. Fail to add a record {i}.\n')
    write_balance(balance)

    if error_exist == True:
        sys.stderr.write('The format of a record should be like this: breakfast -50\n\n')
    else:
        pass

    return 0

#user input 'view'
def user_view():
    print('{:<20}{:<20}'.format('Description', 'Amount'))
    divide()
    with open(file_path, 'r') as fh:
        for line in fh.readlines()[1:]:
            record = line.split(':')
            sys.stdout.write(f'{record[0]:<20}{record[1]}')
    divide()
    balance = read_balance()
    print(f'Now you have {balance} dollars.')
    return 0

#user input 'delete'
def user_delete(user_input):
    lines = []
    del_record = []
    balance = read_balance()                                              #set 'balance' in the func global
    s = user_input.split()
    with open(file_path, 'r') as fh:
        for line in fh.readlines()[1:]:
            lines.append(re.split(':|\n', line)[:2])

    if s in lines:                                             #check if value exist
        last_index = len(lines) - lines[::-1].index(s) - 1          #find the last exist value index
        s[1] = int(s[1])
        balance -= s[1]                                         #count balance
        del(lines[last_index])                                       #delete value

        del_record.append(str(balance) + '\n')
        for i, j in lines:
            s_format = str(i) + ':' + str(j) + '\n'
            del_record.append(s_format)
        with open(file_path, 'w') as fh:
            fh.writelines(del_record)
    else:
        print(f'There is no record with ({s[0]} {s[1]}). Fail to delete a record')
         
    return 0


#main code
#=======================================================================================
#initial account balance
if os.path.exists(file_path):
    print('Welcome back!')
else:
    balance = 0
    try:
        balance = int(input('How many money do you have? '))
    except ValueError:
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
    finally:
        write_balance(balance)


while True:
    user_input = input('What do you want to do (add/view/delete/exit)? ')
    if user_input == 'add':
        user_add(input())
    elif user_input == 'view':
        user_view()
    elif user_input == 'delete':
        try:
            user_delete(input())
        except Exception:
            sys.stderr.write('Wrong format\n')
    elif user_input == 'exit':
        break
    else:
        sys.stderr.write('Invalid command. Try again\n')











