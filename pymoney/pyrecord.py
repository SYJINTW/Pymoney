#!/usr/bin/env python3
import sys
import os.path                                              #check file exist
import copy
import re
import time
from datetime import date

#reset
#=======================================================================================
file_path = '../record.txt'

#class
#=======================================================================================
class Record:
    """Represent a record"""
    def __init__(self, date, category, name, amount):
        self._date = date
        self._category = category
        self._name = name
        self._amount = float(amount)
    
    @property    
    def date(self):
        return self._date

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
            data = list(map(self.clean_newline, data))
            print('Welcome back!\n')
            self._initial_money = float(data[data.index('Balance:')+1])
            self._records = data[data.index('Records:')+1:data.index('SaveTime:')]
        else:
            self._initial_money = 0.0                                           #initial balance
            self._records = []

    def user_add(self, input_data, input_categories):                                         #user input 'add'
        user_inputs = input_data.split(',')
        error_exist = False                                     #error exist flag
        for i in user_inputs:
            try:                                            #set try-except to skip the error data
                user_input = i.split()
                if len(user_input) == 3:
                    user_input.insert(0, str(date.today()))
                elif len(user_input) == 4:
                    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', user_input[0]):
                        sys.stderr.write('The format of date should be YYYY-MM-DD.')
                        raise ValueError
                else:
                    print(user_input)
                    sys.stderr.write('Wrong number of argv.')
                    raise IndexError

                record = Record(*user_input)
                if input_categories.is_category_valid(record.category, input_categories._categories):
                    self._initial_money += record.amount
                    self._records.append(f'{record.date}:{record.category}:{record.name}:{record.amount}')
                else:
                    raise ValueError(f'Invalid value for categories. Fail to add a record {i}.\n')

            except (IndexError,TypeError,ValueError):                              #if the format is wrong
                error_exist = True
                sys.stderr.write(f'Fail to add a record {i}.\n')

        if error_exist == True:                                 #format remind
            sys.stderr.write('The format of a record should be like this: YYYY-MM-DD food breakfast -50\n\n')
        else:
            print('Add Success\n')
        return
    
    def user_view(self):
        print("Here's your expense and income records:")
        print(f'{"Date":<20}{"Category":<20}{"Description":<20}{"Amount":<20}')
        self.divide()
        for line in self._records:
            content = line.split(':')
            print(f'{content[0]:<20}{content[1]:<20}{content[2]:<20}{content[3]}') #date:name:amount:category
        self.divide()
        print(f'Now you have {self._initial_money} dollars.\n')
    
    def user_delete(self, input_data, input_index):                                      #user input 'delete'
        try:
            balance = self._initial_money
            record = copy.deepcopy(self._records)
            new_record = []
            user_input = input_data.split()
            user_input[3] = str(float(user_input[3]))
            lines = []
            count = 0
            for line in record:
                x = line.split(':')
                lines.append(x)
                if x == user_input:
                    count += 1
            if count == 0:
                sys.stderr.write(f'There is no record with ({user_input[0]} {user_input[1]} {user_input[2]} {user_input[3]}). Fail to delete a record\n\n')
                self._records = record
                return
            else:
                if count == 1:
                    lines.pop(lines.index(user_input))
                    balance -= float(user_input[1])
                else:
                    self.divide()
                    count = 1
                    for line in lines:
                        if line == user_input:
                            print(f'{count:<3}{line[2]:<20}{line[0]:<20}{line[1]}')
                            count += 1
                    self.divide()
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
                new_record.append(f'{i[0]}:{i[1]}:{i[2]}:{i[3]}')
            print('Delete Success\n')
            self._initial_money = balance
            self._records = new_record
            return
        except Exception:
                sys.stderr.write('Wrong format\n\n')
    
    def user_reset(self):                                           #user input 'reset'
        if os.path.exists(file_path):
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
                fh.write('SaveTime:\n'+ str(date.today()))
            print('Finish Saving')
            return
        except:
            sys.stderr.write('Fail To Save\n')
    
    def user_find(self, target_categories, view):
        amount = 0.0
        index = 0
        for line in self._records:
            content = line.split(':')
            if content[1] in target_categories:
                view.insert(index, f'{content[0]:<15}{content[1]:<20}{content[2]:<20}{content[3]:<20}')
                amount += float(content[3])
                index += 1
        return amount

    @staticmethod
    def clean_newline(line):
        new_line = line.split('\n')[0]
        return new_line

    @staticmethod
    def divide():                                               #divide line function
        print('='*80)

