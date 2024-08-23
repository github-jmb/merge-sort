import random

def merge(A):
    merge2(A, 0, len(A) - 1)
    return A

def merge2(A, first, last):
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
    L.append(float('inf'))  # Using inf as a sentinel value
    R.append(float('inf'))  # Using inf as a sentinel value

    i = j = 0
    for k in range(first, last + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1

A = random.sample(range(1000), 12)

print('Your list is: ' + str(A) + '\n')
print(merge(A))