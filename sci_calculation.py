import matplotlib
import numpy as np
import pandas as pd
import math
from scipy.signal import butter, lfilter_zi, lfilter
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    zi = lfilter_zi(b, a)
    return b, a, zi

def butter_lowpass_filter(data, cutoff, fs, zeropoint=0, order=4):
    if cutoff==500:
        return data
    else:
        b, a, zi = butter_lowpass(cutoff, fs, order=order)
        y = np.round(lfilter(b, a, data, zi=zeropoint*zi)[0], decimals=4)
    return y


def ProcessASTM(data, dt):
    # if dt > 1999:
    #     x = min(int(dt / 50),90)
    # else:
    x = 5
    data = data.loc[::x, :]
    dt = int(max(dt / x, 1))
    x_array = list(data.iloc[:, 1])
    y_array = list(data.iloc[:, 2])
    z_array = list(data.iloc[:, 3])
    m = len(y_array)

    maxp = np.max(list(
        map(lambda i: [max(min(x_array[i:i + dt]), 0), max(min(y_array[i:i + dt]), 0), max(min(z_array[i:i + dt]), 1)],
            range(m - dt))), axis=0)
    maxn = np.min(list(
        map(lambda i: [min(max(x_array[i:i + dt]), 0), min(max(y_array[i:i + dt]), 0), min(max(z_array[i:i + dt]), 1)],
            range(m - dt))), axis=0)
    return maxp, maxn

def ProcessGB(data, dt):
    # if dt > 999:
    #     x = min(int(dt / 50),90)
    # else:
    x = 5
    data = data.loc[::x, :]
    dt = int(max(dt / x, 1))
    y_array = list(data.iloc[:, 2].values)
    z_array = list(data.iloc[:, 3].values)
    m = len(y_array)

    maxp = np.max(list(map(lambda i: [max(min(y_array[i:i + dt]), 0), max(min(z_array[i:i + dt]), 1)], range(m - dt))),
                  axis=0)
    maxn = np.min(list(map(lambda i: [min(max(y_array[i:i + dt]), 0), min(max(z_array[i:i + dt]), 1)], range(m - dt))),
                  axis=0)
    return maxp, maxn

def append4(x1,x2,x3,x4):
    x=np.append(x1,x2)
    x=np.append(x,x3)
    x=np.append(x,x4)
    return x

def eggXY(x1, x2, y_max):
    x1 = min(x1, 2)
    y_max = min(y_max, 3)

    x11 = np.cos(np.arange(0, math.pi * 0.5, 0.01)) * x2
    x22 = np.cos(np.arange(math.pi * 0.5, math.pi, 0.01)) * x1
    x33 = np.cos(np.arange(math.pi, math.pi * 1.5, 0.01)) * x1
    x44 = np.cos(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * x2
    y11 = np.sin(np.arange(0, math.pi * 0.5, 0.01)) * y_max
    y22 = np.sin(np.arange(math.pi * 0.5, math.pi, 0.01)) * y_max
    y33 = np.sin(np.arange(math.pi, math.pi * 1.5, 0.01)) * y_max
    y44 = np.sin(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * y_max
    return append4(x11, x22, x33, x44), append4(y11, y22, y33, y44)


def eggXZ(x1, x2, y1, y2):
    x1 = min(x1, 2)
    y1 = min(y1, 2)
    y2 = min(y2, 6)
    x11 = np.cos(np.arange(0, math.pi * 0.5, 0.01)) * x2
    x22 = np.cos(np.arange(math.pi * 0.5, math.pi, 0.01)) * x1
    x33 = np.cos(np.arange(math.pi, math.pi * 1.5, 0.01)) * x1
    x44 = np.cos(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * x2
    y11 = np.sin(np.arange(0, math.pi * 0.5, 0.01)) * y2
    y22 = np.sin(np.arange(math.pi * 0.5, math.pi, 0.01)) * y2
    y33 = np.sin(np.arange(math.pi, math.pi * 1.5, 0.01)) * y1
    y44 = np.sin(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * y1

    return append4(x11, x22, x33, x44), append4(y11, y22, y33, y44)


def eggYZ(x, y1, y2):
    y1 = min(2, y1)
    y2 = min(6, y2)
    x = min(3, x)
    x11 = np.cos(np.arange(0, math.pi * 0.5, 0.01)) * x
    x22 = np.cos(np.arange(math.pi * 0.5, math.pi, 0.01)) * x
    x33 = np.cos(np.arange(math.pi, math.pi * 1.5, 0.01)) * x
    x44 = np.cos(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * x
    y11 = np.sin(np.arange(0, math.pi * 0.5, 0.01)) * y2
    y22 = np.sin(np.arange(math.pi * 0.5, math.pi, 0.01)) * y2
    y33 = np.sin(np.arange(math.pi, math.pi * 1.5, 0.01)) * y1
    y44 = np.sin(np.arange(math.pi * 1.5, math.pi * 2 + 0.01, 0.01)) * y1
    return append4(x11, x22, x33, x44), append4(y11, y22, y33, y44)

def coef(height, condition):
    if condition == 'x' or condition == 'y':
        if height <= 32:
            return 0.52
        elif height <= 48:
            return height * 0.03 - 0.44
        else:
            return 1

    if condition == 'z':
        if height <= 32:
            return 0.6
        elif height <= 48:
            return height * 0.025 - 0.2
        else:
            return 1


def coordTransform(pitch, seatback, roll, yaw):
    pitch = pitch/180*np.pi
    seatback=seatback/180*np.pi
    roll=roll/180*np.pi
    yaw=yaw/180*np.pi

    P0 = np.array([0, 0, 1])
    R0A = np.array([[math.cos(yaw), -math.sin(yaw), 0], [math.sin(yaw), math.cos(yaw), 0], [0, 0, 1]])
    RAB = np.array([[1, 0, 0], [0, math.cos(roll), math.sin(roll)], [0, math.sin(roll), math.cos(roll)]])
    RBC = np.array(
        [[math.cos(seatback), 0, math.sin(seatback)], [0, 1, 0], [-math.sin(seatback), 0, math.cos(seatback)]])
    RC0 = (np.dot(np.dot(R0A, RAB), RBC)).T

    return np.round(np.dot(RC0, P0), decimals=4)
