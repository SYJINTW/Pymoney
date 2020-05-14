#!/usr/bin/env python3
import sys
import os.path                                              #check file exist
import copy
import time

#reset
#=======================================================================================
file_path = '../record.txt'                                 #difine file path

#function
#=======================================================================================
def divide():                                               #divide line function
    print('='*60)

def clean_newline(line):
    new_line = line.split('\n')[0]
    return new_line

def initialize():
    if os.path.exists(file_path):                               #check if file exist
        with open(file_path, 'r') as fh:
            data = fh.readlines()
        data = list(map(clean_newline, data))
        print('Welcome back!\n')
        balance = float(data[data.index('Balance:')+1])
        categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transort', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
        record = data[data.index('Records:')+1:data.index('SaveTime:')]
        return balance, categories, record
    else:
        initial_money = 0.0                                           #initial balance
        categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transort', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
        try:
            initial_money = float(input('How much money do you have? '))
        except ValueError:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n\n')
        finally:
            return initial_money, categories, []

def user_add(data):                                         #user input 'add'
    record = copy.deepcopy(data)
    global categories
    user_input = input()
    error_exist = False                                     #error exist flag
    user_input_comma = user_input.split(',')                #set list split by ','
    for i in user_input_comma:
        try:                                            #set try-except to skip the error data
            i = i.split()                               #set list split by ' '
            if len(i) == 3:
                if not find_categories(i[0], categories):
                    raise ValueError(f'Invalid value for categories. Fail to add a record {i}.\n')
                change_initial_money(float(i[-1]))
                record.append(f'{i[1]}:{float(i[2])}:{i[0]}')      #append user input to record
            elif len(i) == 2:
                change_initial_money(float(i[-1]))
                record.append(f'{i[0]}:{float(i[1])}:{"unknown"}')      #append user input to record
            else:
                raise IndexError
        except IndexError:                              #if the format is wrong
            error_exist = True
            sys.stderr.write(f'Invalid format. Fail to add a record {i}.\n')
        except ValueError:                              #if i[1] is not integer
            error_exist = True
            sys.stderr.write(f'Invalid value for money. Fail to add a record {i}.\n')

    if error_exist == True:                                 #format remind
        sys.stderr.write('The format of a record should be like this: food breakfast -50\n\n')
    else:
        print('Add Success\n')
    return record

def user_view(data):                                        #user input 'view'
    record = copy.deepcopy(data)
    balance = initial_money
    print("Here's your expense and income records:")
    print(f'{"Category":<20}{"Description":<20}{"Amount":<20}')
    divide()
    for line in record:
        content = line.split(':')
        print(f'{content[2]:<20}{content[0]:<20}{content[1]}')
    divide()
    print(f'Now you have {balance} dollars.\n')
    return

def user_view_categories(categories, prefix = ()):
    if type(categories) in {list,tuple}:
        i = 0
        for child in categories:
            if type(categories) not in {list,tuple}:
                i += 1
            user_view_categories(child, prefix + (i,))
    else:
        print(' '*4*(len(prefix)-1) + '-' + categories)

def user_delete(data):                                      #user input 'delete'
    try:
        record = copy.deepcopy(data)
        new_record = []
        user_input = input().split()
        user_input[-1] = str(float(user_input[-1]))
        user_input.append(user_input.pop(0))          #[name, cost, category]
        lines = []
        count = 0
        for line in record:
            x = line.split(':')
            lines.append(x)
            if x == user_input:
                count += 1
        if count == 0:
            sys.stderr.write(f'There is no record with ({user_input[2]}{user_input[0]} {user_input[1]}). Fail to delete a record\n\n')
            return record
        else:
            if count == 1:
                lines.pop(lines.index(user_input))
            else:
                divide()
                count = 1
                for line in lines:
                    if line == user_input:
                        print(f'{count:<3}{line[2]:<20}{line[0]:<20}{line[1]}')
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
            new_record.append(f'{i[0]}:{i[1]}:{i[2]}')
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

def user_save(balance, categories, record):
    try:
        with open(file_path, 'w') as fh:
            fh.write('Balance:\n' + str(balance) + '\n')
            fh.write('Categories:\n' + str(categories) + '\n')
            fh.write('Records:\n')
            for line in record:
                fh.write(line + '\n')
            fh.write('SaveTime:\n'+ str(time.ctime()))
        print('Finish Saving')
    except:
        sys.stderr.write('Fail To Save\n')

def change_initial_money(change):
    global initial_money 
    initial_money += change
    return

def find_categories(category, categories):
    if type(categories) == list:
        for v in categories:
            p = find_categories(category, v)
            if p == True:
                index = categories.index(v)
                if index + 1 < len(categories) and type(categories[index + 1]) == list:
                    return flatten(categories[index:index + 2])
                else:
                    return [v]
            if p != []:
                return p
    return True if categories == category else []

def flatten(L):
    if type(L) in {list}:
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    else:
        return [L]
            


#main code
#=======================================================================================
#initial account balance
initial_money, categories, record = initialize()

while True:
    user_input = input('What do you want to do (add/view/view categories/delete/find/reset/exit)? ')
    if user_input == 'add':
        record = user_add(record)
    elif user_input == 'view':
        user_view(record)
    elif user_input == 'view categories':
        user_view_categories(categories) 
    elif user_input == 'delete':
        record = user_delete(record)    
    elif user_input == 'exit':
        user_save(initial_money, categories, record)
        break
    elif user_input == 'reset':
        user_reset()
        break
    elif user_input == 'find':
        user_find(record)
    else:
        sys.stderr.write('Invalid command. Try again\n\n')

print('Bye\n')











