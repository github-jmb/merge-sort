import random
import os
import datetime

def get_list_length():
    while True:
        try:
            length = int(input("How many entries do you want to input? Enter an integer (1-100): "))
            if 1 <= length <= 100:
                return length
            else:
                print("The length must be between 1 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            date_obj = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return date_obj
        except ValueError:
            print("Invalid date format. Please enter the date in MM-DD-YYYY format.")

recursive_call_count = 0

def merge(A):
    global recursive_call_count
    recursive_call_count = 0
    merge2(A, 0, len(A) - 1)
    return A

def merge2(A, first, last):
    global recursive_call_count
    recursive_call_count += 1
    if first < last:
        middle = (first + last) // 2
        merge2(A, first, middle)
        merge2(A, middle + 1, last)
        merge3(A, first, middle, last)

def merge3(A, first, middle, last):
    L = A[first:middle + 1]
    R = A[middle + 1:last + 1]
   
    L_readable = [(name, date.strftime("%m-%d-%Y")) for name, date in L]
    R_readable = [(name, date.strftime("%m-%d-%Y")) for name, date in R]
    
    print('L is: ' + str(L_readable))
    print('R is: ' + str(R_readable))
    
    if isinstance(L[0], tuple) and isinstance(R[0], tuple):
        L.append((None, datetime.datetime.max))  # Use max datetime for the sentinel
        R.append((None, datetime.datetime.max))  # Use max datetime for the sentinel
    else:
        L.append(float('inf'))  # Use inf for the sentinel with integers
        R.append(float('inf'))  # Use inf for the sentinel with integers

    i = j = 0
    for k in range(first, last + 1):
        if isinstance(L[i], tuple) and isinstance(R[j], tuple):
            if L[i][1] <= R[j][1]: 
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
        else:
            if L[i] <= R[j]: 
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1

mode = input("Do you want to sort random numbers (type 'random') or names with birthdays (type 'names')? ").strip().lower()

if mode == 'random':
    list_length = get_list_length()
    original_list = random.sample(range(1000), list_length)
    list_to_sort = original_list.copy()
elif mode == 'names':
    list_length = get_list_length()
    original_list = []
    for _ in range(list_length):
        name = input("Enter the name: ")
        birthday = get_date_input("Enter the birthday (MM-DD-YYYY): ")
        original_list.append((name, birthday))
    list_to_sort = original_list.copy()
else:
    print("Invalid mode selected. Exiting.")
    exit(1)

sorted_list = merge(list_to_sort)

formatted_original_list = [(name, date.strftime("%m-%d-%Y")) if isinstance(date, datetime.datetime) else date for name, date in original_list]
formatted_sorted_list = [(name, date.strftime("%m-%d-%Y")) if isinstance(date, datetime.datetime) else date for name, date in sorted_list]

json_data = (
    '{\n'
    '    "original_list": ' + str(formatted_original_list).replace(' ', '') + ',\n'
    '    "sorted_list": ' + str(formatted_sorted_list).replace(' ', '') + '\n'
    '}'
)

file_path = 'sorted_lists.json'  

try:
    with open(file_path, 'w') as file:
        file.write(json_data)

    absolute_path = os.path.abspath(file_path)
    print(f"\nFile created successfully at: {absolute_path}")
    
    with open(file_path, 'r') as file:
        file_contents = file.read()
    print("\nFile Contents:\n", file_contents)
    
except Exception as e:
    print(f"An error occurred: {e}")

print('\nOriginal list:', formatted_original_list)
print('Sorted list:', formatted_sorted_list)
print('Total number of recursive calls:', recursive_call_count)