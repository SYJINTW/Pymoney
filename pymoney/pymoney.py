#!/usr/bin/env python3
import sys
import tkinter
from tkinter import ttk
from datetime import date
from pyrecord import Record
from pyrecord import Records
from pycategory import *

#function
#=======================================================================================
def update_result_box(records_data):
    global delete_flag
    delete_flag = True
    amount = records._initial_money
    for index, line in enumerate(records_data):
        content = line.split(':')
        result_box.insert(index, f'{content[0]:<15}{content[1]:<20}{content[2]:<20}{content[3]:<20}') #date:name:amount:category
    total_str.set(f'Now you have {amount} dollars.')

def clear_result_box():
    result_box.delete(0, 'end')

def clear_text_input():
    find_entry.delete(0,'end')
    date_str.set(str(date.today()))
    description_entry.delete(0,'end')
    amount_entry.delete(0,'end')

def initial_call_back():
    if not records._records:
        try:
            records._initial_money = float(initial_str.get())
            update_result_box(records._records)
        except ValueError:
            pass

def add_call_back():
    user_input = f'{date_str.get()} {category_combobox.get()} {description_str.get()} {amount_str.get()}'
    records.user_add(user_input, categories)
    clear_result_box()
    update_result_box(records._records)
    clear_text_input()

def delete_call_back():
    try:
        if delete_flag:
            index = result_box.curselection()[0]
            records._initial_money -= float(records._records[index].split(':')[3])
            del records._records[index]
            clear_result_box()
            update_result_box(records._records)

    except IndexError:
        pass

def find_call_back():
    global delete_flag
    delete_flag = False
    user_input = f'{find_str.get()}'
    clear_result_box()
    target_categories = categories.find_categories(user_input, categories._categories)
    amount = records.user_find(target_categories, result_box)
    total_str.set(f'The total are {amount} dollars.')

def reset_call_back():
    clear_result_box()
    update_result_box(records._records)
    clear_text_input()

def clean_call_back():
    global save_flag
    records.user_clean()
    save_flag = False
    root.quit()

#initial
#=======================================================================================
records = Records()
categories = Categories()
delete_flag = True
save_flag = True

#tkinter UI
#=======================================================================================
root = tkinter.Tk()
root.title('PyMoney')
root.resizable(False, False)
window = tkinter.Frame(root, borderwidth=5)
window.grid(row = 0, column = 0)

#find
find_label = tkinter.Label(window, text = 'Find category')
find_label.grid(row = 0, column = 0, sticky = tkinter.W)

find_str = tkinter.StringVar()
find_entry = tkinter.Entry(window, textvariable = find_str)
find_entry.grid(row = 0, column = 1, sticky = tkinter.E+tkinter.W)

find_btn = tkinter.Button(window, text = 'Find', command = find_call_back)
find_btn.grid(row = 0, column = 2)

#reset
reset_btn = tkinter.Button(window, text = 'Reset', command = reset_call_back)
reset_btn.grid(row = 0, column = 3)

#result
x_scroll = tkinter.Scrollbar(window, orient = tkinter.HORIZONTAL)
x_scroll.grid(row = 8, column = 0, columnspan = 3, sticky = tkinter.N+tkinter.E+tkinter.W)
y_scroll = tkinter.Scrollbar(window)
y_scroll.grid(row = 1, column = 3, rowspan = 7, sticky = tkinter.N+tkinter.S+tkinter.W)

result_box = tkinter.Listbox(window, xscrollcommand = x_scroll.set, yscrollcommand = y_scroll.set)
result_box.grid(row = 1, column = 0, rowspan = 7, columnspan = 3, sticky = tkinter.E+tkinter.W)

x_scroll.config(command = result_box.xview)
y_scroll.config(command = result_box.yview)

#total
total_str = tkinter.StringVar()
total_entry = tkinter.Label(window, textvariable = total_str)
total_entry.grid(row = 9, column = 0, columnspan = 2, sticky = tkinter.W)

#delete
delete_btn = tkinter.Button(window, text = 'Delete', command = delete_call_back)
delete_btn.grid(row = 9, column = 3, sticky = tkinter.W)

#initial
initial_label = tkinter.Label(window, text = 'Initial money')
initial_label.grid(row = 0, column = 4, sticky = tkinter.W)

initial_str = tkinter.StringVar()
initial_entry = tkinter.Entry(window, textvariable = initial_str)
initial_entry.grid(row = 0, column = 5, sticky = tkinter.E+tkinter.W)

update_btn = tkinter.Button(window, text = 'Update', command = initial_call_back)
update_btn.grid(row = 1, column = 5, sticky = tkinter.N+tkinter.E)

#date
date_label = tkinter.Label(window, text = 'Date')
date_label.grid(row = 3, column = 4, sticky = tkinter.W)

date_str = tkinter.StringVar()
date_str.set(str(date.today()))
date_entry = tkinter.Entry(window, textvariable = date_str)
date_entry.grid(row = 3, column = 5, sticky = tkinter.E+tkinter.W)

#category
category_label = tkinter.Label(window, text = 'Category')
category_label.grid(row = 4, column = 4, sticky = tkinter.W)

category_combobox = ttk.Combobox(window, value = categories.flatten(categories._categories))
category_combobox.grid(row = 4, column = 5, sticky = tkinter.E+tkinter.W)

#description
description_label = tkinter.Label(window, text = 'Description')
description_label.grid(row = 5, column = 4, sticky = tkinter.W)

description_str = tkinter.StringVar()
description_entry = tkinter.Entry(window, textvariable = description_str)
description_entry.grid(row = 5, column = 5, sticky = tkinter.E+tkinter.W)

#amount
amount_label = tkinter.Label(window, text = 'Amount')
amount_label.grid(row = 6, column = 4, sticky = tkinter.W)

amount_str = tkinter.StringVar()
amount_entry = tkinter.Entry(window, textvariable = amount_str)
amount_entry.grid(row = 6, column = 5, sticky = tkinter.E+tkinter.W)

#add
add_btn = tkinter.Button(window, text = 'Add a record', command = add_call_back)
add_btn.grid(row = 7, column = 5, sticky = tkinter.E)

#clean data
clean_btn = tkinter.Button(window, text = 'Clean', command = clean_call_back)
clean_btn.grid(row = 9, column = 5, sticky = tkinter.E)

#=======================================================================================
update_result_box(records._records)
window.mainloop()
if save_flag:
    records.user_save(categories._categories)
    



