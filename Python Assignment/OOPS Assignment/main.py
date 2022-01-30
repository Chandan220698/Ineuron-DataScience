from pkg_dataCollection import mylist
from pkg_dataCollection import myTuple
from pkg_dataCollection import mySet
from pkg_dataCollection import myDict

# LIST
list1 = mylist.customList([1,2,3,4])  # creating customlist

print(list1.display())    # Display will return [1,2,3,4]
list1.appendList(123)     # Appending 123 to list
print(list1.display())    # Display will return [1,2,3,4, 123]
list1.appendList([3+5j, 'data'])     # Appending more data
print(list1.display())    # Display will return the appended list


print("-------------------------------------------------------------------------------------------------------")
# Tuple
tuple1 = myTuple.customTuple((4,5,6,6,6,7,1,7))
print(tuple1.countData(6))
print(tuple1.countData(7))

print("-------------------------------------------------------------------------------------------------------")
# Set
set1 = mySet.customSet({1,1,1,2,2,3,6,9})
print(set1.display())            # Display will return {1,2,3,6,9}
set1.popSet()                    # Removing the last element
print(set1.display())

print("-------------------------------------------------------------------------------------------------------")
# Dict
d = {'k1': 123, 'k2': 'data k2', 'k3': 111}
dict1 = myDict.customDict(d)
print(dict1.display())          # Print the dict1

items = dict1.getItems()
print(items)