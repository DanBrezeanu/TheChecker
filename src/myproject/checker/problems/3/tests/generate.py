import os
import random

random.seed()

for t in range(0, 10):
    el = []
    n = random.randrange(0, 3 ** t) + 5
    for _ in range(0, n):
        el.append(random.randrange(0, 10000))

    with open('3_{}.in'.format(t), 'w') as f:
        f.write(str(n) + '\n')
        for i in el:
            f.write(str(i) + ' ')

        f.write('\n')

    even = list(filter(lambda x: x % 2 == 0, el))
    odd = list(filter(lambda x: x % 2 == 1, el))

    even.sort()
    odd.sort(reverse = True)

    with open('3_{}.out'.format(t), 'w') as f:
        for i in even:
            f.write(str(i) + ' ')
        f.write('\n')
        for i in odd:
            f.write(str(i) + ' ')
        f.write('\n')


