import multiprocessing
import requests
import time
import json
from monitor import monitor
from random import randint

# ----------------------- Q-LEARNING --------------------------
from random import randint

servers = 4
fractal = 1
NumEpisodes = 2000

# Environment Class ------------------------------
class Environment:
    def __init__(self,servers,fractal):
        self.servers = servers
        self.fractal = fractal
    def getActions(self,s_now,f_now,time):
        poss_actions = []
        if(time<2.5 and s_now>1 and f_now==fractal):
            for s_decrease in range(1,s_now+1):
                x = [-1*(s_decrease),0]
                poss_actions.append(x)
            return poss_actions
        if(time>2.5 and s_now<servers):
            for s_increase in range(1,5-s_now):
                x = [s_increase,0]
                poss_actions.append(x)
            return poss_actions
        if(time>2.5 and s_now==servers):
            for f_decrease in range(1,min(int(f_now*10),5)+1):
                x = [0,-1*round(f_decrease*(0.1),1)]
                poss_actions.append(x)
            return poss_actions
        if(time<2.5 and f_now<fractal):
            for f_increase in range(1,min(10-int(f_now*10),5)+1):
                x = [0,round(f_increase*(0.1),1)]
                poss_actions.append(x)
            return poss_actions
        return [[0,0]]

    def getRewards(self,s_now,f_now,time):
        if(time <= 2.5):
            return (100 + 25*(f_now))/s_now
        else:
            return -10

# Brain Class --------------------------------
class Brain:
    def __init__(self,alpha,gamma):
        self.Qtable = dict()
        self.alpha = alpha
        self.gamma = gamma
    def updateQvalue(self,i,j,a,i1,j1,r):
        key1 = str(i)+":"+str(j)+":"+str(a)
        maxQ = -1
        for s_change in range(-4,4):
            for f_change in range(-5,5):
                keychk = str(i1)+":"+str(j1)+":"+str([s_change,f_change*0.1])
                maxQ = max(maxQ,self.Qtable.get(keychk,0))
        self.Qtable[key1] = (1-self.alpha)*self.Qtable.get(key1,0) + self.alpha*(r + self.gamma*(maxQ))
    def makeTransitionMax(self,s_now,f_now,time,actions):
        maxi = -1
        for a in actions:
            keyi = str(s_now) + ":" + str(f_now) + ":" +str(time)+":"+ str(a)
            Qval = self.Qtable.get(keyi,0)
            maxi = max(maxi,Qval)
        for a in actions:
            keyi = str(s_now) + ":" + str(f_now) + ":" +str(time)+":"+ str(a)
            Qval = self.Qtable.get(keyi,0)
            if(Qval == maxi):
                return s_now + a[0], round(f_now + a[1],1), a
        return s_now, f_now, [0,0]

# Agent Class ---------------------------------------------------
class Agent:
    def __init__(self):
        pass
    def makeTransitionRandom(self,s_now,f_now,actions):
        n = len(actions)
        if(n==1):
            x = 0
        else:
            x = randint(0,n-1)
        a = actions[x]
        return s_now + a[0], round(f_now + a[1],1), a

# Main function -----------------------------------------

environment = Environment(servers,fractal)
agent = Agent()
brain = Brain(0.1,0.9)
epsilon = 0.4
decay = 0.999


def agentMakeTransition(time,s_now,f_now):
    chk = randint(1, 10)
    if (chk <= 10 * epsilon):
        actions = environment.getActions(s_now, f_now, time)
        i1, j1, a = agent.makeTransitionRandom(s_now, f_now, actions)
        return i1,j1,a

    else:
        actions = environment.getActions(s_now,f_now,time)
        try:
            x = brain.makeTransitionMax(s_now, f_now, time,actions)
            i1, j1, a = x
        except:
            print(x)
        return i1,j1,a


def updateQvalue(s_old,f_old,a,s_new,f_new,t_new):
    r = environment.getRewards(s_new, f_new, t_new)
    brain.updateQvalue(s_old, f_old, a, s_new, f_new, r)



# ----------------------------------------------------------------

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
        old_servers = -1
        old_fs = -1
        init_servers = 1
        init_fs = 1
        cnt =1
        for line in fp:
            q = line.split(' ')
            for i in range(len(q)-1):
                q[i] = int(q[i])
            q[-1] = int(q[-1][:-1])
            #num_of_servers = [1,2,3,4]
            if(init_servers<1):
                init_servers = 1
            Ns = init_servers
            pool = multiprocessing.Pool(processes=Ns)
            n1 = len(q)
            q = q[:int(n1*init_fs)+1]
            inputs = []
            for i in range(len(q)):
                inputs.append([q[i],(i%Ns)+1])
            start_time = time.time()
            outputs = pool.map(serve, inputs)
            t = (time.time() - start_time)
            print(t,"s for request:",cnt)
            t = round(t,1)
            print("servers:",init_servers,"fraction:",init_fs)
            if(cnt>=2):
                updateQvalue(old_servers,old_fs,action_taken,init_servers,init_fs,t)
            init_servers,init_fs,action_taken = agentMakeTransition(t,init_servers,init_fs)
            old_servers, old_fs = init_servers, init_fs
            time_window=[]
            cnt +=1
    with open("sample.json", "w") as outfile:
        json.dump(brain.Qtable, outfile)
