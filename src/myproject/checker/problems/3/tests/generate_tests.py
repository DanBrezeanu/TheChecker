import os, random
from subprocess import Popen

prefix = "2_"

random.seed()

for i in range(0, 10):
    elements = []
    n = random.randrange(0, 4 ** i)

    for _ in range(n):
        e = random.randrange(0, 10 ** 9)
        if i == 7 or i == 9:
            while e % 2 == 0:
                e = random.randrange(0, 10 ** 9)

        elements.append(e)

    with open('2.in', 'w') as f:
        for e in elements:
            f.write(str(e) + ' ')

        f.write('0\n')

    p = Popen('./a.out')
    p.wait()

    os.rename('2.out', prefix + str(i) + '.out')
    os.rename('2.in', prefix + str(i) + '.in')
