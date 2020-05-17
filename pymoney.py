#!/usr/bin/env python3
import sys
import os.path                                              #check file exist
import copy
import time

#reset
#=======================================================================================
file_path = '../record.txt'                                 #define file path

#class
#=======================================================================================
class Record:
    """Represent a record"""
    def __init__(self, category, name, amount):
        self._category = category
        self._name = name
        self._amount = float(amount)
    
    @property    
    def category(self):
        return self._category

    @property    
    def name(self):
        return self._name
    
    @property    
    def amount(self):
        return self._amount
    

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        if os.path.exists(file_path):                               #check if file exist
            with open(file_path, 'r') as fh:
                data = fh.readlines()
            data = list(map(clean_newline, data))
            print('Welcome back!\n')
            self._initial_money = float(data[data.index('Balance:')+1])
            self._records = data[data.index('Records:')+1:data.index('SaveTime:')]
        else:
            self._initial_money = 0.0                                           #initial balance
            self._records = []
            try:
                self._initial_money = float(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n\n')

    def user_add(self, input_data, input_categories):                                         #user input 'add'
        categories = copy.deepcopy(input_categories._categories)
        user_input = input_data.split(',')
        error_exist = False                                     #error exist flag
        for i in user_input:
            try:                                            #set try-except to skip the error data
                record = Record(*(i.split()))
                if input_categories.find_categories(record.category, categories):
                    print('a')
                    self._initial_money += record.amount
                    self._records.append(f'{record.name}:{record.amount}:{record.category}')
                else:
                    raise ValueError(f'Invalid value for categories. Fail to add a record {i}.\n')

            except (IndexError,TypeError):                              #if the format is wrong
                error_exist = True
                sys.stderr.write(f'Invalid format. Fail to add a record {i}.\n')
            except ValueError:                              #if i[1] is not integer
                error_exist = True
                sys.stderr.write(f'Invalid value for money. Fail to add a record {i}.\n')

        if error_exist == True:                                 #format remind
            sys.stderr.write('The format of a record should be like this: food breakfast -50\n\n')
        else:
            print('Add Success\n')
        return
    
    def user_view(self):
        print("Here's your expense and income records:")
        print(f'{"Category":<20}{"Description":<20}{"Amount":<20}')
        divide()
        for line in self._records:
            content = line.split(':')
            print(f'{content[2]:<20}{content[0]:<20}{content[1]}')
        divide()
        print(f'Now you have {self._initial_money} dollars.\n')
    
    def user_delete(self, input_data):                                      #user input 'delete'
        try:
            balance = self._initial_money
            record = copy.deepcopy(self._records)
            new_record = []
            user_input = input_data.split()
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
                self._records = record
                return
            else:
                if count == 1:
                    lines.pop(lines.index(user_input))
                    balance -= float(user_input[1])
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
                    balance -= float(user_input[1])
            for i in lines:
                new_record.append(f'{i[0]}:{i[1]}:{i[2]}')
            print('Delete Success\n')
            self._initial_money = balance
            self._records = new_record
            return
        except Exception:
                sys.stderr.write('Wrong format\n\n')
        
    def user_reset(self):                                           #user input 'reset'
        os.remove(file_path)
        print(f'{file_path} has been Removed')
        
    def user_save(self, categories):
        try:
            with open(file_path, 'w') as fh:
                fh.write('Balance:\n' + str(self._initial_money) + '\n')
                fh.write('Categories:\n' + str(categories) + '\n')
                fh.write('Records:\n')
                for line in self._records:
                    fh.write(line + '\n')
                fh.write('SaveTime:\n'+ str(time.ctime()))
            print('Finish Saving')
            return
        except:
            sys.stderr.write('Fail To Save\n')
    
    def user_find(self, target_categories):
        print("Here's your expense and income records:")
        print(f'{"Category":<20}{"Description":<20}{"Amount":<20}')
        amount = 0.0
        divide()
        for line in self._records:
            content = line.split(':')
            if content[2] in target_categories:
                print(f'{content[2]:<20}{content[0]:<20}{content[1]}')
                amount += float(content[1])
        divide()
        print(f'Now you have {amount} dollars.\n')


class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transport', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
        #if os.path.exists(file_path):                               #check if file exist
        #    with open(file_path, 'r') as fh:
        #        data = fh.readlines()
        #    self._categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transport', ['bus', 'railway']], 'income', ['salary', 'bonus'], 'unknown']
        
    def user_view_categories(self, categories, prefix = ()):
        if type(categories) in {list,tuple}:
            i = 0
            for child in categories:
                if type(categories) not in {list,tuple}:
                    i += 1
                self.user_view_categories(child, prefix + (i,))
        else:
            print(' '*4*(len(prefix)-1) + '-' + categories)

    def find_categories(self, category, categories):
        if type(categories) == list:
            for v in categories:
                p = self.find_categories(category, v)
                if p == True:
                    index = categories.index(v)
                    if index + 1 < len(categories) and type(categories[index + 1]) == list:
                        return self.flatten(categories[index:index + 2])
                    else:
                        return [v]
                if p != []:
                    return p
        return True if categories == category else []

    def flatten(self, L):
        if type(L) in {list}:
            result = []
            for child in L:
                result.extend(self.flatten(child))
            return result
        else:
            return [L]


#function
#=======================================================================================
def divide():                                               #divide line function
    print('='*60)

def clean_newline(line):
    new_line = line.split('\n')[0]
    return new_line


#main code
#=======================================================================================
#initial account balance
records = Records()
categories = Categories()
while True:
    user_input = input('What do you want to do (add/view/view categories/delete/find/reset/exit)? ')
    if user_input == 'add':
        add_record = input()
        records.user_add(add_record, categories)
    elif user_input == 'view':
        records.user_view()
    elif user_input == 'view categories':
        categories.user_view_categories(categories._categories) 
    elif user_input == 'delete':
        delete_record = input('Which record do you want to delete?\n')
        records.user_delete(delete_record)    
    elif user_input == 'exit':
        records.user_save(categories._categories)
        break
    elif user_input == 'reset':
        records.user_reset()
        break
    elif user_input == 'find':
        category = input('Which category do you want to find?\n')
        target_categories = categories.find_categories(category, categories._categories)
        records.user_find(target_categories)
    else:
        sys.stderr.write('Invalid command. Try again\n\n')

print('Bye\n')











