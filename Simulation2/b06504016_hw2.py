import math
import random
import numpy as np
import matplotlib.pyplot as plt
def dbmtowatt(dbm):
        return math.pow(10, dbm/10) / 1000
def dbtowatt(dbm):
        return math.pow(10, dbm/10)
def watttodb(watt):
        return 10 * math.log10(watt) 
Pt = dbmtowatt(33)
Pu = dbmtowatt(23)
Gt = dbtowatt(14)
Gr = dbtowatt(14)
T = 300
B = pow(10, 7)
ht = 50 + 1.5
hr = 1.5
noise = 1.38 * pow(10, -23) * T * B 
X = []
Y = []

class MD:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance = math.sqrt(x**2+y**2)
        self.power_r = 0
        self.power_t = 0
        self.inter = 0
    def dis_bs(self, bs_x, bs_y):
        return math.sqrt((bs_x - self.x)**2+(bs_y - self.y)**2)  
def power(d):
    return Pt*Gt*Gr*((ht * hr) ** 2) /(d ** 4)
def power_bs(d):
    return Pu*Gt*Gr*((ht * hr) ** 2) /(d ** 4)    
class BS:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.total_power = 0 #Watt
        self.inter = 0
        self.md = []
base = []
base.append(BS(0, 0))
base.append(BS(0, 500))
base.append(BS(0, 1000))
base.append(BS(0, -500))
base.append(BS(0, -1000))
base.append(BS(-250 * math.sqrt(3), 250))
base.append(BS(-250 * math.sqrt(3), -250))
base.append(BS(-250 * math.sqrt(3), -750))
base.append(BS(-250 * math.sqrt(3), 750))
base.append(BS(250 * math.sqrt(3), 250))
base.append(BS(250 * math.sqrt(3), -250))
base.append(BS(250 * math.sqrt(3), 750))
base.append(BS(250 * math.sqrt(3), -750))
base.append(BS(500 * math.sqrt(3), 0))
base.append(BS(500 * math.sqrt(3), 500))
base.append(BS(500 * math.sqrt(3), -500))
base.append(BS(-500 * math.sqrt(3), 0))
base.append(BS(-500 * math.sqrt(3), 500))
base.append(BS(-500 * math.sqrt(3), -500))           
for bs in base:
    for i in range(50):
        x = random.uniform(-250/math.sqrt(3), 500/math.sqrt(3))
        y = random.uniform(-250, 250)
        if y > -x * math.sqrt(3) + 500:
            x = x - 750/math.sqrt(3)
            y = y - 250
        if y < x * math.sqrt(3) - 500:
            x = x - 750/math.sqrt(3) 
            y = y + 250 
        bs.md.append(MD(x + bs.x, y + bs.y))
#1-1
for device in base[0].md:
    X.append(device.x)
    Y.append(device.y)
plt.scatter(X, Y)
plt.axis('square')
plt.scatter(0, 0, marker='^', color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.title('1-1')
plt.savefig('./1-1.jpg')
plt.figure() 
#1-2
X1 = []
Y1 = []
for md in base[0].md:
    X1.append(md.distance)
    md.power_r = power(md.distance)
    Y1.append(watttodb(md.power_r))  
plt.scatter(X1, Y1)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('1-2')
plt.savefig('./1-2.jpg')
plt.figure()
#1-3
X2 = []
Y2 = []
for md in base[0].md:
    I = 0
    for bs in base:
        I = I + power(math.sqrt((md.x - bs.x) ** 2 + (md.y - bs.y) ** 2))
    I = I - md.power_r + noise
    X2.append(md.distance)
    md.inter = watttodb(I)
    Y2.append(watttodb(md.power_r) - md.inter)
plt.scatter(X2, Y2)
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.title('1-3')
plt.savefig('./1-3.jpg')
plt.figure()
#2-1
plt.scatter(X, Y)
plt.scatter(0, 0, marker='^', color='r')
plt.axis('square')
plt.xlabel('x')
plt.ylabel('y')
plt.title('2-1')
plt.savefig('./2-1.jpg')
plt.figure() 
#2-2
X3 = []
Y3 = []
for md in base[0].md:
    X3.append(md.distance)
    md.power_t = power_bs(md.distance)
    Y3.append(watttodb(md.power_t))          
plt.scatter(X3, Y3)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('2-2')
plt.savefig('./2-2.jpg')
plt.figure()
#2-3
X4 = []
Y4 = []
for md in base[0].md:   
    base[0].total_power = base[0].total_power + md.power_t
  
for md in base[0].md:    
    X4.append(md.distance)
    I = watttodb(base[0].total_power - md.power_t + noise) 
    Y4.append(watttodb(md.power_r) - I)
plt.scatter(X4, Y4)
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.title('2-3')
plt.savefig('./2-3.jpg')
plt.figure()
#bonus1
X5 = []
X6 = []
Y5 = []
Y6 = []
for bs in base:
    X5.append(bs.x)
    Y5.append(bs.y)
    for md in bs.md:
        X6.append(md.x)
        Y6.append(md.y)
plt.scatter(X5, Y5, marker='^', color='r')
plt.scatter(X6, Y6, marker = '.', linewidths = 0)
plt.axis('square')
plt.xlabel('x')
plt.ylabel('y')
plt.title('bonus1')
plt.savefig('./bonus1.jpg')
plt.figure()        
#bonus2
X7 = []
Y7 = []
for bs in base:
    for md in bs.md:
        X7.append(md.dis_bs(bs.x, bs.y))
        md.power_t = power_bs(md.dis_bs(bs.x, bs.y))
        Y7.append(watttodb(md.power_t))          
plt.scatter(X7, Y7, marker = '.', linewidths = 0)
plt.xlabel('distance(m)')
plt.ylabel('power(dB)')
plt.title('bonus2')
plt.savefig('./bonus2.jpg')
plt.figure()
#bonus3
X8 = []
Y8 = []
i = []

for bs in base:
    I = 0
    for md in bs.md:
        I = I + power_bs(md.dis_bs(bs.x, bs.y))
    bs.total_power = I
for bs in base:    
    for md in bs.md:
        X8.append(md.dis_bs(bs.x, bs.y))
        I = bs.total_power - md.power_t + noise 
        Y8.append(watttodb(md.power_t) - watttodb(I)) 
plt.scatter(X8, Y8, marker = '.', linewidths = 0)
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.title('bonus3')
plt.savefig('./bonus3.jpg')
plt.show()