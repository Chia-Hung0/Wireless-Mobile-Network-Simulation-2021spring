import math
import random
import numpy as np
import matplotlib.pyplot as plt


def dbmtowatt(dbm):
        return math.pow(10, dbm / 10) / 1000


def dbtowatt(dbm):
        return math.pow(10, dbm / 10)


def watttodb(watt):
        return 10 * math.log10(watt)


def power_bs(d):
    return Pu * Gt * Gr * ((ht * hr) ** 2) /(d ** 4)


def change_direction():
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(min_speed, max_speed)
    time = random.randint(min_time, max_time)
    return angle, speed, time

Simulation_time = 900
Pu = dbmtowatt(23)
Gt = dbtowatt(14)
Gr = dbtowatt(14)
T = 300
B = pow(10, 7)
ht = 50 + 1.5
hr = 1.5
noise = 1.38 * pow(10, -23) * T * B
min_speed = 1
max_speed = 15
min_time = 1
max_time = 6


class Map:
    def __init__(self):
        self.cluster = []

    def add_cluster(self, cluster):
        self.cluster.append(cluster)

    def generate_cluster(self):
        self.add_cluster(Cluster(0, 0, graph))
        self.add_cluster(Cluster(4.5 * 500/math.sqrt(3), 1750, graph))
        self.add_cluster(Cluster(-3 * 500/math.sqrt(3), 2000, graph))
        self.add_cluster(Cluster(-7.5 * 500/math.sqrt(3), 250, graph))
        self.add_cluster(Cluster(-4.5 * 500/math.sqrt(3), -1750, graph))
        self.add_cluster(Cluster(3 * 500/math.sqrt(3), -2000, graph))
        self.add_cluster(Cluster(7.5 * 500/math.sqrt(3), -250, graph))

    def init_base(self):
        for cluster in self.cluster:
            for bs in cluster.base:
                bs.add_neighbor()

    def get_center_cluster(self):
        return self.cluster[0]
class Cluster:
    def __init__(self, x, y, map):
        self.base = []
        self.map = map
        self.x = x
        self.y = y
        self.generate_base()
    def generate_md(self):
        for i in range(100):
            bs = self.base[random.randint(0, 18)]
            md = MD(bs, self.map, i+1)
            bs.add_md(md)

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
        self.neighbor = []

    def add_md(self, md):
        self.md.append(md)

    def add_neighbor(self):
        for cluster in self.cluster.map.cluster:
            for bs in cluster.base:
                if math.sqrt((bs.x - self.x) ** 2 + (bs.y - self.y) ** 2) <= 1000:
                    self.neighbor.append(bs)
class MD:
    def __init__(self, bs, map, num):
        self.x, self.y = generate_location()
        self.x += bs.x
        self.y += bs.y
        self.bs = bs
        self.map = map
        self.angle, self.speed, self.time = change_direction()
        self.num = num

    def dis_bs(self, bs_x, bs_y):
        return math.sqrt((bs_x - self.x)**2+(bs_y - self.y)**2)

    def change_bs(self, time, count, event):
        if self.time == 0:
            self.angle, self.speed, self.time = change_direction()
            x_speed = self.speed * math.cos(self.angle)
            y_speed = self.speed * math.sin(self.angle)
            self.x += x_speed
            self.y += y_speed
            self.time -= 1
        else:
            x_speed = self.speed * math.cos(self.angle)
            y_speed = self.speed * math.sin(self.angle)
            self.x += x_speed
            self.y += y_speed
            self.time -= 1
        max_sinr = -1 * math.inf
        max_bs = self.bs
        for bs in self.bs.neighbor:
            dis = math.sqrt((self.x - bs.x) ** 2 + (self.y - bs.y) ** 2)
            sinr = SINR(power_bs(dis), total_power(self.map, bs))
            if sinr > max_sinr:
                max_sinr = sinr
                max_bs = bs
        original_dis = math.sqrt((self.x - self.bs.x) ** 2 + (self.y - self.bs.y) ** 2)
        original_sinr = SINR(power_bs(original_dis), total_power(self.map, self.bs))
        if max_sinr > original_sinr + 6:
            event = add_event(event, self.num, time, self.bs.num, max_bs.num)
            self.bs.md.remove(self)
            self.bs = max_bs
            self.bs.add_md(self)
            count += 1
        return count

def add_event(event, num, time, init_bs, handoff_bs):
    event.append((num, time, init_bs, handoff_bs))
    print("ID : {:3}, Time : {:3}, Before : {:2}, After : {:2}".format(num, time, init_bs, handoff_bs))
    return event


def generate_location():
    x = random.uniform(-250/math.sqrt(3), 500/math.sqrt(3))
    y = random.uniform(-250, 250)
    if y > -x * math.sqrt(3) + 500:
        x = x - 750/math.sqrt(3)
        y = y - 250
    if y < x * math.sqrt(3) - 500:
        x = x - 750/math.sqrt(3)
        y = y + 250
    return x, y


def total_power(map, Bs):
    inf = 0
    for cluster in map.cluster:
        for bs in cluster.base:
            for md in bs.md:
                distance = math.sqrt((md.x - Bs.x) ** 2 + (md.y - Bs.y) ** 2)
                inf += power_bs(distance)
    return inf


def SINR(power, inf):
    inf = inf - power
    return watttodb(power/(inf+noise))


def plot_map(graph):
    bs_x = []
    bs_y = []
    md_x = []
    md_y = []
    for bs in graph.base:
        bs_x.append(bs.x)
        bs_y.append(bs.y)
        for m in bs.md:
            md_x.append(m.x)
            md_y.append(m.y)
    plt.scatter(bs_x, bs_y, color='r', marker='^')
    for bs in graph.base:
        plt.annotate(bs.num, (bs.x, bs.y))
    plt.axis('square')
    plt.title('Map')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./bonus_1.jpg')
    plt.figure()
    plt.scatter(bs_x, bs_y, color='r', marker='^')
    plt.scatter(md_x, md_y, marker='.')
    for bs in graph.base:
        plt.annotate(bs.num, (bs.x, bs.y))
    plt.axis('square')
    plt.title('Map')
    plt.xlabel("X(m)")
    plt.ylabel("Y(m)")
    plt.savefig('./bonus_2.jpg')
    plt.show()


def output_file(Handoff):
    f = open("list.txt", "w")
    for i in Handoff:
        f.write("ID : {:3}, Time : {:3}, Before : {:2}, After : {:2}\n".format(i[0], i[1], i[2], i[3]))
    f.write("Total handoff {} times.".format(count))
    print("Total handoff {} times.".format(count))
    f.close()


if __name__ == "__main__":
    graph = Map()
    graph.generate_cluster()
    graph.init_base()
    center = graph.get_center_cluster()
    center.generate_md()
    plot_map(center)
    count = 0
    Handoff = {}
    for i in range(100):
        Handoff = []
    for time in range(1, Simulation_time+1):
        for cluster in graph.cluster:
            for bs in cluster.base:
                for md in bs.md:
                    count = md.change_bs(time, count, Handoff)
    output_file(Handoff)
