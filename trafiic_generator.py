from random import randint

n = 100
switch = 1
for i in range(n):
    q = []
    if(i%10 == 0):
        switch = -1*switch
    if(switch == 1):
        q = []
        for j in range(1000):
            q.append((randint(12340000, 123456700)))
        print(*q, sep=" ")
    else:
        q = []
        for j in range(10):
            q.append((randint(1234, 2345)))

        print(*q, sep=" ")


