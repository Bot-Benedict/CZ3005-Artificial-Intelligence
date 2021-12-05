import json
from collections import defaultdict

f1 = open('../data/G.json')
f2 = open('../data/Coord.json')
f3 = open('../data/Dist.json')
f4 = open('../data/Cost.json')
MAX_BUDGET = 287932

G = json.load(f1)
Coord = json.load(f2) # h(n)
Dist = json.load(f3) # g(n)
Cost = defaultdict(int, json.load(f4))