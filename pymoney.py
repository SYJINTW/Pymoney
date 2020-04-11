import sys

record = [['a',20],['a',20],['a',20],['a',20],['a',20]]

def divide():
    print('='*40)

#user input 'add'
def user_add(s):
    s = s.split(',')
    for i in s:
        i = i.split()
        i[1] = int(i[1])
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
    return 0




#initial account balance
balance = 0
balance = int(input('How many money do you have? '))
while True:
    user_input = input('What do you want to do (add/view/delete/exit)?')
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











