"""
Created by Moritz Wenzel 24.February 2020

This short program samples digits form Pi and then plots them as coordinates on a unit circle/square.
Then the points are counted and the actual value of Pi approximated with the ratio of points in the circle and total
points."""

"""Import some packages"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib import rc
rc('text', usetex=True)

"""Read in PI digits"""
f = open('Pi_1e6.txt')
Pi_rand = str(f.read())


"""Sample some numbers
sample defines how many numbers will be sampled (how many darts will be thrown on the board)"""
sample = 750

# digits = 5
""" a_step and b_step tell the sampling how many digits need to be stepped through 
until a new set of 5 digits is sampled.
a_seed and b_seed tell the sampling where to start."""
a_step = 17
b_step = 17
a_seed = 65
b_seed = 70

"""Y counts how many points land inside the unit circle
N counts how many points land outside the unit circle
Ycount and Ncount save the distribution of Y and N for each step
a, b, x, and y then collect the coordinates for the points"""
Y = 0
N = 0
Ycount = np.zeros(sample)
Ncount = np.zeros(sample)
a = np.zeros(sample, dtype=int)
b = np.zeros(sample, dtype=int)
x = np.zeros(sample)
y = np.zeros(sample)

"""Drawing of numbers from Pi, saving them and computing the distribution of Y and N"""
for Iter in range(sample):
    a[Iter] = a_step * Iter + a_seed
    b[Iter] = b_step * Iter + b_seed
    x[Iter] = (float(Pi_rand[a[Iter]] + Pi_rand[a[Iter] + 1]
                     + Pi_rand[a[Iter] + 2] + Pi_rand[a[Iter] + 3] + Pi_rand[a[Iter] + 4]))
    y[Iter] = (float(Pi_rand[b[Iter]] + Pi_rand[b[Iter] + 1]
                     + Pi_rand[b[Iter] + 2] + Pi_rand[b[Iter] + 3] + Pi_rand[b[Iter] + 4]))

    if (x[Iter] - 50000) ** 2 + (y[Iter] - 50000) ** 2 <= 50000 ** 2:
        Y = Y + 1
        Ycount[Iter] = Y
        Ncount[Iter] = Ncount[Iter - 1]

    else:
        N = N + 1
        Ncount[Iter] = N
        Ycount[Iter] = Ycount[Iter - 1]

""" Plot the value of Pi obtained for the last sample"""
pi = round((Ycount[-1] * 4) / (Ncount[-1] + Ycount[-1]), 4)
print(pi)


"""Animation"""
an = np.linspace(0, 2 * np.pi, 100)
fig, ax = plt.subplots(1, 1)

ax.set_aspect('equal', 'box')
plt.xticks([0, 100000], [0, 1])
plt.yticks([0, 100000], [0, 1])

scatter1, = ax.plot([], [], 'o', c='g', alpha=0.2)
scatter2, = ax.plot([], [], 'o', c='r', alpha=0.2)


def init():
    ax.plot(50000 * np.cos(an) + 50000, 50000 * np.sin(an) + 50000, c='k')
    scatter1.set_data([], [])
    scatter2.set_data([], [])
    return scatter1, scatter2,


x_plot1 = []
y_plot1 = []
x_plot2 = []
y_plot2 = []


def PiAni(Iter):

    if (x[Iter] - 50000) ** 2 + (y[Iter] - 50000) ** 2 <= 50000 ** 2:
        x_plot1.append(x[Iter])
        y_plot1.append(y[Iter])
        scatter1.set_data(x_plot1[:], y_plot1[:])

    else:
        x_plot2.append(x[Iter])
        y_plot2.append(y[Iter])
        scatter2.set_data(x_plot2[:], y_plot2[:])

    pi = round((Ycount[Iter] * 4) / (Ncount[Iter] + Ycount[Iter]), 4)
    plt.title(r'$\pi = \frac{Red}{Red+Green} 4 = $' + str('{:.4f}'.format(pi)))
    return scatter1, scatter2,


Iter = sample
anim = ani.FuncAnimation(fig, PiAni, init_func=init, frames=Iter, interval=0.01, blit=True)

FFMpegWriter = ani.writers['ffmpeg']
writer = FFMpegWriter(bitrate=-1, fps=100, codec="libx264", extra_args=['-pix_fmt', 'yuv420p'])

anim.save('PiThon' + str(sample) + '.mp4', writer=writer)
