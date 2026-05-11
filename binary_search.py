arr_example = [0, 12, 23, 35, 111, 192]
'''
we need to find 14 (not in the list in this case)
'''


def binary_search(arr_example, target):
    start = 0
    end = len(arr_example)
    index1 = 0
    while start<end and (end-start)//2>0:
        curr_index = start+(end-start)//2
        current = arr_example[curr_index]
        
        if current<target:
            start = curr_index
            print(curr_index)
        elif current>target:
            end = curr_index
        else:
            return curr_index

        index1 += 1
    return -1
        
   

print(binary_search(arr_example, 111))