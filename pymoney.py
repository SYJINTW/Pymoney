#!/usr/bin/env python3
import sys

#reset
#=======================================================================================
record = [['a',20],['a',30],['a',20],['a',20],['a',30]]



#function
#=======================================================================================
def divide():
    print('='*40)


#user input 'add'
def user_add(s):
    global balance                                              #set 'balance' in the func global
    s = s.split(',')
    for i in s:
        i = i.split()
        i[i] = int(i[1])
        balance += i[1]
        record.append(i)
    return 0

#user input 'view'
def user_view():
    print('{:<20}{:<20}'.format('Description', 'Amount'))
    divide()
    for i, j in record:
        print('{:<20}{:<20}'.format(i, j))
    divide()
    print(f'Now you have {balance} dollars.')
    return 0

#user input 'delete'
def user_delete(s):
    global balance                                              #set 'balance' in the func global
    s = s.split()
    s[1] = int(s[1])
    if s in record:                                             #check if value exist
        last = len(record) - record[::-1].index(s) - 1          #find the last exist value index
        balance -= s[1]                                         #count balance
        del(record[last])                                       #delete value
    else:
        pass

    return 0


#main code
#=======================================================================================
#initial account balance
balance = 0
balance = int(input('How many money do you have? '))
while True:
    user_input = input('What do you want to do (add/view/delete/exit)? ')
    if user_input == 'add':
        user_add(input())
    elif user_input == 'view':
        user_view()
    elif user_input == 'delete':
        user_delete(input())
    elif user_input == 'exit':
        break
    else:
        sys.stderr.write('Input unknown keywords.')











