import random
import os
import datetime
from faker import Faker

def get_list_length():
    while True:
        try:
            length = int(input("How many random entries do you want to generate? Enter an integer (1-100): "))
            if 1 <= length <= 100:
                return length
            else:
                print("The length must be between 1 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

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
    
    if isinstance(L[0], tuple):
        L_readable = [(name, date.strftime("%m-%d-%Y")) for name, date in L]
        R_readable = [(name, date.strftime("%m-%d-%Y")) for name, date in R]
        L.append((None, datetime.datetime.max))  # Sentinel for tuple lists
        R.append((None, datetime.datetime.max))  # Sentinel for tuple lists
    else:
        L_readable = L
        R_readable = R
        L.append(float('inf'))  # Sentinel for integer lists
        R.append(float('inf'))  # Sentinel for integer lists
    
    print('L is: ' + str(L_readable))
    print('R is: ' + str(R_readable))

    i = j = 0
    for k in range(first, last + 1):
        if isinstance(L[0], tuple):  
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

fake = Faker()

mode = input("Do you want to sort random numbers (type 'random') or generate random names with birthdays (type 'names')? ").strip().lower()

if mode == 'random':
    list_length = get_list_length()
    original_list = random.sample(range(1000), list_length)
    list_to_sort = original_list.copy()
elif mode == 'names':
    list_length = get_list_length()
    original_list = [
        (fake.name(), datetime.datetime.combine(fake.date_of_birth(minimum_age=0, maximum_age=100), datetime.datetime.min.time()))
        for _ in range(list_length)
    ]
    list_to_sort = original_list.copy()
else:
    print("Invalid mode selected. Exiting.")
    exit(1)

sorted_list = merge(list_to_sort)

formatted_original_list = [
    (name, date.strftime("%m-%d-%Y")) if isinstance(date, datetime.datetime) else date for name, date in original_list
] if mode == 'names' else original_list

formatted_sorted_list = [
    (name, date.strftime("%m-%d-%Y")) if isinstance(date, datetime.datetime) else date for name, date in sorted_list
] if mode == 'names' else sorted_list

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