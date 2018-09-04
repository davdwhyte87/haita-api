numArray1 =[3,9,8]
numArray2 =[8,12,74]
N=3
sumArray = []

# Write the logic here:
for i in range(N):
    c=i
    s= numArray1[c] + numArray2[c]
    sumArray.append(s)

# Print the sumArray
for element in sumArray:
    print(element, end=" ")

print("")