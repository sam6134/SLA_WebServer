import matplotlib.pyplot as plt
from math import log
import numpy as np
from random import randint
import pickle
import time
# use ggplot style for more sophisticated visuals
with open('fractalStream.pkl', 'rb') as f:
   dfFractal = pickle.load(f)
with open('serverStream.pkl', 'rb') as f:
   dfServer = pickle.load(f)
with open('trafficStream.pkl', 'rb') as f:
   dfTrafiic = pickle.load(f)
with open('TimeStream.pkl', 'rb') as f:
   dfTime = pickle.load(f)


plt.style.use('ggplot')
plt.ion()
fig, ax = plt.subplots()
fig.canvas.set_window_title('Live Chart')
ax.set_title("Servers")
df=[]
df1=[]
for i in range(len(dfTime)):
    df.append([dfServer[i]])
    df1.append([log(dfTrafiic[i],3)])
    ax.plot(df, '-o')
    ax.plot(df1,'b')
    plt.show()
    plt.pause(0.0001)
    time.sleep(.4)



plt.style.use('ggplot')
plt.ion()
fig, ax = plt.subplots()
fig.canvas.set_window_title('Live Chart')
ax.set_title("Server data")
df=[]
df1=[]
for i in range(len(dfTime)):
    df.append([dfTime[i]])
    df1.append([2.5])
    ax.plot(df, '-o')
    ax.plot(df1,'b')
    plt.show()
    plt.pause(0.0001)
    time.sleep(.4)

