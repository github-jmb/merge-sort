import random
import os

def get_list_length():
    while True:
        try:
            length = int(input("How long do you want your list to be? Enter an integer (1-100): "))
            if 1 <= length <= 100:
                return length
            else:
                print("The length must be between 1 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

list_length = get_list_length()

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
    print('L is: ' + str(L))
    print('R is: ' + str(R))
    L.append(float('inf'))
    R.append(float('inf'))

    i = j = 0
    for k in range(first, last + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1

original_list = random.sample(range(1000), list_length)
list_to_sort = original_list.copy()

sorted_list = merge(list_to_sort)

json_data = (
    '{\n'
    '    "original_list": ' + str(original_list).replace(' ', '') + ',\n'
    '    "sorted_list": ' + str(sorted_list).replace(' ', '') + '\n'
    '}'
)

file_path = 'sorted_lists.json'  

try:
    with open(file_path, 'w') as file:
        file.write(json_data)

    absolute_path = os.path.abspath(file_path)
    print(f"File created successfully at: {absolute_path}")
    
    with open(file_path, 'r') as file:
        file_contents = file.read()
    print("\nFile Contents:\n", file_contents)
    
except Exception as e:
    print(f"An error occurred: {e}")

print('Original list:', original_list)
print('Sorted list:', sorted_list)
print('Total number of recursive calls:', recursive_call_count)
