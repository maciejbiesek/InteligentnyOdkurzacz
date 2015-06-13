import random
from bisect import *


def GrayCodeRank(myArray):
    r = 0
    b = 0
    n = len(myArray)

    for i in range(n - 1, -1, -1):
        if myArray[n - i - 1] == 1:
            b = 1 - b
        if b == 1:
            r += (1 << i)
    return r


class Chromosome:
    def __init__(self, n=0):
        self.bits = [0] * n

    def randomize(self):
        for i in range(0, len(self.bits)):
            self.bits[i] = random.randint(0, 1)

    def length(self):
        return len(self.bits)

    def append(self, v):
        self.bits.extend(v)

    def setPart(self, pos, v):
        self.bits[pos:pos + len(v)] = v

    def getPart(self, pos, count):
        return self.bits[pos:pos + count]

    def printBits(self):
        print(self.bits)


def Crossover(c1, c2, crossover_rate):
    if random.random() <= crossover_rate:
        assert (c1.length() == c2.length())
        k = random.randint(0, c1.length() - 1)
        c1.bits[k:], c2.bits[k:] = c2.bits[k:], c1.bits[k:]

def Mutation(c, mutation_rate):
    for i in range(0, c.length()):
        if random.random() <= mutation_rate:
            c.bits[i] = 1 - c.bits[i]


def FitnessSelection(fitness):
    t = fitness[:]
    n = len(t)
    for i in range(0, n):
        if t[i] < 0:
            t[i] = 0
    for i in range(1, n):
        t[i] += t[i - 1]
    f = random.random() * t[-1]
    i = bisect_left(t, f)
    if i >= n:
        i = n - 1
    return i
