import numpy as np 

def findnumber(arr, nums):
    x = np.sort(np.array(arr))
    d = np.diff(x)
    ind = np.where(d>1)
    neues_array = []
    for num in ind[0]:
        new = range(x[num]+1, x[num+1])
        neues_array += [n for n in new]

    l = len(neues_array)
    if nums <= l:
        return neues_array[0:nums]

    maxnum = x[-1]
    neues_array += [n for n in range(maxnum+1, maxnum+nums-l+1)]
    return neues_array


arr = findnumber([1,2,3,7,6,9,10,12,15,14,18,19,20,25,26],3)
print(arr)