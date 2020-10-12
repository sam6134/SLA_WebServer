import multiprocessing
import requests
import time
from random import randint

def serve(x):
    if(x[1]==1):
        temp =requests.get("http://0.0.0.0:5050/prime/"+str(x[0]))
        return temp.text
    elif(x[1] == 2):
        temp = requests.get("http://0.0.0.0:5051/prime/" + str(x[0]))
        return temp.text
    elif(x[1] == 3):
        temp = requests.get("http://0.0.0.0:5052/prime/" + str(x[0]))
        return temp.text
    elif (x[1] == 4):
        temp = requests.get("http://0.0.0.0:5053/prime/" + str(x[0]))
        return temp.text


if __name__ == '__main__':
    with open("traffic1.txt") as fp:
        cnt =1
        for line in fp:
            q = line.split(' ')
            for i in range(len(q)-1):
                q[i] = int(q[i])
            q[-1] = int(q[-1][:-1])
            num_of_servers = [1,2,3,4]
            Ns = num_of_servers[3]
            pool = multiprocessing.Pool(processes=Ns)
            inputs = []
            for i in range(len(q)):
                inputs.append([q[i],(i%Ns)+1])
            start_time = time.time()
            outputs = pool.map(serve, inputs)
            print(time.time() - start_time,"s for request:",cnt)
            pool.terminate()
            cnt +=1