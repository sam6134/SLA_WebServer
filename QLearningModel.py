from random import randint

servers = 4
fractal = 10
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
            for f_decrease in range(1,min(int(f_now*10),5)):
                x = [0,-1*f_decrease*(0.1)]
                poss_actions.append(x)
            return poss_actions
        if(time<2.5 and f_now<fractal):
            for f_increase in range(1,min(10-int(f_now*10),5)):
                x = [0,f_increase*(0.1)]
                poss_actions.append(x)

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
        keyU = str(i1) + ":" + str(j1) + ":" + "U"
        keyD = str(i1) + ":" + str(j1) + ":" + "D"
        keyL = str(i1) + ":" + str(j1) + ":" + "L"
        keyR = str(i1) + ":" + str(j1) + ":" + "R"
        maxQ = max(self.Qtable.get(keyD,0),self.Qtable.get(keyU,0),self.Qtable.get(keyL,0),self.Qtable.get(keyR,0))
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
                return s_now + a[0], f_now + a[1], a

# Agent Class ---------------------------------------------------
class Agent:
    def __init__(self):
        pass
    def makeTransitionRandom(self,s_now,f_now,actions):
        n = len(actions)
        x = randint(0,n-1)
        a = actions[x]
        return s_now + a[0], f_now + a[1], a

# Main function -----------------------------------------

environment = Environment(servers,fractal)
agent = Agent()
brain = Brain(0.1,0.9)
epsilon = 0.9
decay = 0.999

for episodes in range(NumEpisodes):
    Total_reward = 0
    curr_i =0
    curr_j =0
    while(True):
        if(curr_i == (environment.Nx-1) and curr_j == (environment.Ny-1)):
            break
        chk = randint(1,10)
        if(chk<=10*epsilon):
            actions = environment.getActions(curr_i,curr_j)
            i1,j1,a = agent.makeTransitionRandom(curr_i,curr_j,actions)
            r = environment.getRewards(i1,j1)
            Total_reward += r
            brain.updateQvalue(curr_i,curr_j,a,i1,j1,r)
        else:
            actions = environment.getActions(curr_i,curr_j)
            i1,j1,a = brain.makeTransitionMax(curr_i,curr_j,actions)
            r = environment.getRewards(i1, j1)
            Total_reward += r
            brain.updateQvalue(curr_i, curr_j, a, i1, j1, r)
        curr_i, curr_j = i1,j1
    epsilon = epsilon*decay
    if(episodes%100 == 0):
        print(episodes,"episodes are done")
        print("Reward Collected during this episode is",Total_reward)