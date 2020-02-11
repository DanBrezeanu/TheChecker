import os, random
from subprocess import Popen

prefix = "1_"

random.seed()

for i in range(0, 10):
    elements = []
    n = random.randrange(0, 4 ** i) + 1

    for _ in range(n):
        e = random.randrange(0, 2 * 10 ** 9) - 10 ** 9
        elements.append(e)

    with open('1.in', 'w') as f:
        for e in elements:
            f.write(str(e) + '\n')

        f.write('0\n')

    p = Popen('./a.out')
    p.wait()

    os.rename('1.out', prefix + str(i) + '.out')
    os.rename('1.in', prefix + str(i) + '.in')
