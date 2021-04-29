import math
import numpy as np
import matplotlib.pyplot as plt
def dbmtowatt(dbm):
    return math.pow(10, dbm/10) / 1000
def dbtowatt(dbm):
    return math.pow(10, dbm/10)
def watttodb(watt):
    return 10 * math.log10(watt)
def tworay_gd(ht, hr, d):
    return ((ht * hr) ** 2) /(d ** 4)   
def power(gd, Pt, Gt, Gr):
    return Pt * Gt * Gt * gd
Pt = dbmtowatt(33)
Gt = dbtowatt(14)
Gr = dbtowatt(14)
ht = 50 + 1.5
hr = 1.5
T = 300
B = pow(10, 7)
noise = 1.38 * pow(10, -23) * T * B 
#1-1 1-2
x1 = np.linspace(1, 100, 500) 
x2 = np.linspace(1, 100, 500) 
y1 = np.empty((1, 0))
for i in x1:
    y1 = np.append(y1, watttodb(power(tworay_gd(ht, hr, i), Pt, Gt, Gr)))
y2 = y1 - watttodb(noise)
plt.plot(x1, y1)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('1-1')
plt.figure()
plt.plot(x2, y2)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('1-2')
plt.figure()
#2-1 2-2 
mu, sigma = 0., 6.  
x3 = np.linspace(1, 100, 500) 
y3 = y1 + np.random.normal(mu, sigma, 500)
plt.plot(x3, y3)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('2-1')
plt.figure()
x4 = np.linspace(1, 100, 500) 
y4 = np.empty((1, 0))
for i in y3:
    y4 = np.append(y4, i - watttodb(noise))
plt.plot(x4, y4)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('2-2')
plt.show()