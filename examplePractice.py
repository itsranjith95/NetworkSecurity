l = [1, 2,3,4,5]
print("HI")
print('provide the index of the list element you want to access')
i = int(input())

try:
    print(l[i])
except Exception as e:
    print("There is a runtime error:", e)
print("Bye")