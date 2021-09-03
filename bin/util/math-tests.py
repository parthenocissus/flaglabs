import math
from scipy.special import expit, logit


def map_proportion(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


results = [sigmoid(0), sigmoid(10), sigmoid(-10)]
results2 = [expit(0), expit(10), expit(-10)]
results3 = [logit(0), logit(0.01), logit(0.25), logit(0.5), logit(0.75), logit(0.99), logit(1)]

for r in results:
    r = '{:f}'.format(r)
    print(r)

print()

for r in results2:
    r = '{:f}'.format(r)
    print(r)

print()

for r in results3:
    r = '{:f}'.format(r)
    print(r)
