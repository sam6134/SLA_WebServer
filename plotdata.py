import pickle
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

def estimate_coef(x, y):

    n = np.size(x)
    m_x, m_y = np.mean(x), np.mean(y)

    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


def plot_regression_line(x, y, b):

    plt.scatter(x, y, color="m",
                marker="o", s=30)

    y_pred = b[0] + b[1] * x

    plt.plot(x, y_pred, color="g")


    plt.xlabel('Fraction change')
    plt.ylabel('Time Overhead')

    plt.show()


flag=True
with open('data.pkl', 'rb') as f:
   data = pickle.load(f)
if(flag==True):
    fractal_data = []
    for i in data:
        if(i[0] == 'F'):
            if(i[2]>=5*i[1] and i[2]<=8*i[1]):
                fractal_data.append(i[1:])
    x = [i[0] for i in fractal_data]
    y = [i[1] for i in fractal_data]


    x = np.array(x)
    y = np.array(y)

    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
        \nb_1 = {}".format(b[0], b[1]))

    plot_regression_line(x, y, b)

else:
    server_data=[]
    for i in data:
        if(i[0]=='S'):
            server_data.append(i[1:])
    z = [i[0] for i in server_data]
    x = [i[1] for i in server_data]
    y = [i[2] for i in server_data]

    fig = plt.figure(figsize=(16, 9))
    ax = plt.axes(projection="3d")


    ax.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.3,
            alpha=0.2)


    my_cmap = plt.get_cmap('hsv')

    sctt = ax.scatter3D(x, y, z,
                        alpha=0.8,
                        c=(x),
                        cmap=my_cmap,
                        marker='^')

    plt.title("3D")
    ax.set_xlabel('Server Load', fontweight='bold')
    ax.set_ylabel('Time Overhead', fontweight='bold')
    ax.set_zlabel('Optimal Server Load', fontweight='bold')
    fig.colorbar(sctt, ax=ax, shrink=0.5, aspect=5)

    plt.show()

