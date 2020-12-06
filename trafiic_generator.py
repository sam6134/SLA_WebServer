from random import randint

n = 100
switch = -1
for i in range(100):
    if(i%10 == 0):
        switch = -1*switch
    q=[]
    if(switch==1):
        for j in range(100):
            q.append(randint(1000,5000))
    else:
        for j in range(1000):
            q.append(randint(1000, 10000))
    print(*(q),sep=" ")


