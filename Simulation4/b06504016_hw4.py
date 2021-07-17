import math
import random
import numpy as np
import matplotlib.pyplot as plt

def dbmtowatt(dbm):
    return math.pow(10, dbm / 10) / 1000


def dbtowatt(dbm):
    return math.pow(10, dbm / 10)


def watttodb(watt):
    return 10 * math.log2(watt)

Pt = dbmtowatt(33)
Gt = dbtowatt(14)
Gr = dbtowatt(14)
T = 300
B = 1E7
ht = 50 + 1.5
hr = 1.5
noise = 1.38 * pow(10, -23) * T * B
n = 50
buffer = 6 * 1E6
Xl = 1E6
Xm = 2*1E6
Xh = 3*1E6
time = 1000

def power_bs(d):
    return Pt * Gt * Gr * ((ht * hr) ** 2) /(d ** 4)

class Cluster:
    def __init__(self, x, y):
        self.base = []
        self.x = x
        self.y = y

    def generate_base(self):
        self.base.append(BS(self.x + 0,self.y + 0, 1, self))
        self.base.append(BS(self.x+0, self.y+500, 2, self))
        self.base.append(BS(self.x+0, self.y+1000, 3, self))
        self.base.append(BS(self.x+0, self.y-500, 4, self))
        self.base.append(BS(self.x+0, self.y-1000, 5, self))
        self.base.append(BS(self.x-250 * math.sqrt(3), self.y+250, 6, self))
        self.base.append(BS(self.x-250 * math.sqrt(3), self.y-250, 7, self))
        self.base.append(BS(self.x-250 * math.sqrt(3), self.y-750, 8, self))
        self.base.append(BS(self.x-250 * math.sqrt(3), self.y+750, 9, self))
        self.base.append(BS(self.x+250 * math.sqrt(3), self.y+250, 10, self))
        self.base.append(BS(self.x+250 * math.sqrt(3), self.y-250, 11, self))
        self.base.append(BS(self.x+250 * math.sqrt(3), self.y+750, 12, self))
        self.base.append(BS(self.x+250 * math.sqrt(3), self.y-750, 13, self))
        self.base.append(BS(self.x+500 * math.sqrt(3), self.y+0, 14, self))
        self.base.append(BS(self.x+500 * math.sqrt(3), self.y+500, 15, self))
        self.base.append(BS(self.x+500 * math.sqrt(3), self.y-500, 16, self))
        self.base.append(BS(self.x-500 * math.sqrt(3), self.y+0, 17, self))
        self.base.append(BS(self.x-500 * math.sqrt(3), self.y+500, 18, self))
        self.base.append(BS(self.x-500 * math.sqrt(3), self.y-500, 19, self))


class BS:
    def __init__(self, x, y, num, cluster):
        self.num = num
        self.x = x
        self.y = y
        self.md = []
        self.cluster = cluster

    def add_md(self):
        for i in range(n):
            x = random.uniform(-250/math.sqrt(3), 500/math.sqrt(3))
            y = random.uniform(-250, 250)
            if y > -x * math.sqrt(3) + 500:
                x = x - 750/math.sqrt(3)
                y = y - 250
            if y < x * math.sqrt(3) - 500:
                x = x - 750/math.sqrt(3)
                y = y + 250
            md = MD(self, x, y)
            self.md.append(md)

class MD:
    def __init__(self, bs, x, y):
        self.x = x + bs.x
        self.y = y + bs.y
        self.bs = bs
        self.distance = math.sqrt((bs.x - self.x)**2+(bs.y - self.y)**2)
        self.power = power_bs(self.distance)
        self.rate = 0
        self.totalpower = 0
        self.sinr = 0
        self.buffer = np.zeros(3)
        
    def dis_bs(self, bs_x, bs_y):
        return math.sqrt((bs_x - self.x)**2+(bs_y - self.y)**2)

    def shannon_rate(self, band):
        self.rate = band*math.log2(1+self.sinr)

    def total_power(self, cluster):
        inf = 0
        for bs in cluster.base:
                d = math.sqrt((self.x - bs.x) ** 2 + (self.y - bs.y) ** 2)
                inf += power_bs(d)
        self.totalpower = inf
        inf = self.totalpower - self.power
        self.sinr = self.power/(inf+noise)
        self.shannon_rate(B/n)



def plot_map():
    bs_x = []
    bs_y = []
    md_x = []
    md_y = []
    clu = Cluster(0, 0)
    clu.generate_base()
    for bs in clu.base:
        bs_x.append(bs.x)
        bs_y.append(bs.y)
    clu.base[0].add_md()
    for md in clu.base[0].md:
        md_x.append(md.x)
        md_y.append(md.y)
    plt.scatter(bs_x, bs_y, color = 'r',marker = '^')
    plt.scatter(md_x, md_y, marker = '.')
    plt.axis('square')
    plt.title('Map 1-1')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./1-1.jpg')
    plt.figure()

    x = []
    y = []
    for md in clu.base[0].md:
        md.total_power(clu)
        x.append(md.distance)
        y.append(md.rate)
    plt.scatter(x, y)
    plt.title('Shannon Rate 1-2')
    plt.xlabel("distance(m)")
    plt.ylabel("rate(bits/s)")
    plt.savefig('./1-2.jpg')
    plt.figure()

    current_buff = np.zeros(3)
    loss_counter = np.zeros(3)
    Total_data = np.zeros(3)
    load = np.array([Xl, Xm, Xh])
    for i in range(time):
        for md in clu.base[0].md: 
            for i in range(3):
                if load[i]>=md.rate:
                    md.buffer[i] += load[i]- md.rate
                    current_buff[i] += load[i]- md.rate  
                if load[i]<md.rate:      
                    if md.buffer[i] >  md.rate - load[i]:
                        md.buffer[i] += load[i]- md.rate
                        current_buff[i] += load[i]- md.rate 
                    else:
                        md.buffer[i] = 0       
                if current_buff[i] > buffer:
                    loss_counter[i] += current_buff[i] - buffer
                    current_buff[i] = buffer
            Total_data += load       
    plt.bar(['Light', 'Middle', 'Heavy'], loss_counter/Total_data , color = ['lightgreen', 'yellow', 'red'])
    plt.title('Packet Loss Probability 1-3')
    plt.ylabel('P')
    plt.xlabel('Load')
    plt.savefig('./1-3.jpg')
    plt.figure()

def plot_bonus():
    bs_x = []
    bs_y = []
    md_x = []
    md_y = []
    clu = Cluster(0, 0)
    clu.generate_base()
    for bs in clu.base:
        bs_x.append(bs.x)
        bs_y.append(bs.y)
    clu.base[0].add_md()
    for md in clu.base[0].md:
        md_x.append(md.x)
        md_y.append(md.y)
    plt.scatter(bs_x, bs_y, color = 'r',marker = '^')
    plt.scatter(md_x, md_y, marker = '.')
    plt.axis('square')
    plt.title('Map B-1')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./B-1.jpg')
    plt.figure()

    x = []
    y = []
    for md in clu.base[0].md:
        md.total_power(clu)
        x.append(md.distance)
        y.append(md.rate)
    plt.scatter(x, y)
    plt.title('Shannon Rate B-2')
    plt.xlabel("distance(m)")
    plt.ylabel("rate(bits/s)")
    plt.savefig('./B-2.jpg')
    plt.figure()

    current_buff = np.zeros(3)
    loss_counter = np.zeros(3)
    Total_data = np.zeros(3)
    for i in range(time):
        for md in clu.base[0].md: 
            p1 = np.random.poisson(1E6, 1)
            p2 = np.random.poisson(2*1E6, 1)
            p3 = np.random.poisson(3*1E6, 1)
            p = np.array([p1[0], p2[0], p3[0]])
            for i in range(3):
                if p[i]>=md.rate:
                    md.buffer[i] += p[i]- md.rate
                    current_buff[i] += p[i]- md.rate  
                if p[i]<md.rate:      
                    if md.buffer[i] >  md.rate - p[i]:
                        md.buffer[i] += p[i]- md.rate
                        current_buff[i] += p[i]- md.rate 
                    else:
                        current_buff[i] -= md.buffer[i]
                        md.buffer[i] = 0       
                if current_buff[i] > buffer:
                    loss_counter[i] += current_buff[i] - buffer
                    current_buff[i] = buffer
            Total_data += p 
    plt.bar(['Light', 'Middle', 'Heavy'], loss_counter/Total_data , color = ['lightgreen', 'yellow', 'red'])
    plt.title('Packet Loss Probability B-3')
    plt.ylabel('P')
    plt.xlabel('Load')
    plt.savefig('./B-3.jpg')
    plt.show()    


if __name__ == "__main__":
    plot_map()
    plot_bonus()
    
