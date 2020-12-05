import pickle
import numpy as np
from sklearn.linear_model import LinearRegression



class Model:
    def __init__(self):
        pass
    def FitModel(self):
        with open('data.pkl', 'rb') as f:
           data = pickle.load(f)

        server_data=[]
        for i in data:
            if(i[0]=='S'):
                server_data.append(i[1:])
        x = np.array([[i[1],i[2]] for i in server_data])
        y = np.array([i[0] for i in server_data])
        model = LinearRegression().fit(x, y)
        r_sq = model.score(x, y)
        print('coefficient of determination:', r_sq)
        print('c0:', model.intercept_)
        print('Coeffecients', model.coef_)
def DetermineCoeff():
    m = Model()
    m.FitModel()


class Controller:
    def __init__(self):
        self.t_ref = 2.5
        self.I = 0.8
        self.D = 0.8
        self.errorS =[]
        self.errorF = []
    def GlobalController(self,t,init_server,init_fs):

        x = self.Scontroller(t,init_server)
        y = self.Fcontroller(t,init_fs)
        return x,y


    def Scontroller(self,t,init_servers):
        u_t = (t-self.t_ref)
        v_t = init_servers
        add_I=0
        add_D=0
        if(len(self.errorS)>0):
            add_I = self.I*sum(self.errorS)
        if(len(self.errorS)>1):
            add_D = self.D*(self.errorS[-1] - self.errorS[-2])
        v_t1 = int(0.8*v_t + 0.39*(u_t) + 1.5 + add_I + add_D)
        if(t>self.t_ref and init_servers<4):
            self.errorS.append(t-self.t_ref)
        if(t<self.t_ref and init_servers>1):
            self.errorS.append(t - self.t_ref)
        if(v_t1>4):
            v_t1 = 4
        if(v_t1<1):
            v_t1 = 1
        return v_t1

    def Fcontroller(self,t,init_fs):
        u_t = (t-self.t_ref)
        add_I = 0
        add_D = 0
        if (len(self.errorF) > 0):
            add_I = self.I*sum(self.errorF)
        if (len(self.errorF) > 1):
            add_D = self.D*(self.errorF[-1] - self.errorF[-2])
        f_t1 = (init_fs - 0.615*(u_t) + 0.03 - add_I - add_D)
        if(t>self.t_ref and init_fs>0.1):
            self.errorF.append(t-self.t_ref)
        if(t<self.t_ref and init_fs<1):
            self.errorF.append(t - self.t_ref)
        if(f_t1<0.1):
            f_t1 = 0.1
        if(f_t1>1):
            f_t1 = 1
        return f_t1


