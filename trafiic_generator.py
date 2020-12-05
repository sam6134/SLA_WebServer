from random import randint

n = 100
switch = 1
for i in range(n):
    q = []
    if(i%5 == 0):
        n1 = randint(100,1000)
    if(i%5 == 0):
        low = randint(1000,100000)
    for j in range(n1):
        q.append(randint(low,low*10))
    print(*(q),sep=" ")


