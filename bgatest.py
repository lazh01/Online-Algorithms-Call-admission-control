from bga import bga
from graphbldr import Graph_Builder
import random
import math
import matplotlib.pyplot as plt

def gen_call(g, calls):
    call_list = []
    for i in range(calls):
        samples = random.sample(list(g.nodes), 2)
        call = g.call(samples[0], samples[1], 1, 1)
        call_list += [call]
    return call_list


call_count = []
res = []
nodes = 1000
increment = 100
limit = nodes
count = 0
ncalls = 0
while ncalls != limit:
        print(count)
        ncalls += increment
        results = []
        for i in range(30):
                graphbldr = Graph_Builder()
                g = graphbldr.build_line(nodes,1)
                calls = gen_call(g, ncalls )
                alg = bga(g, nodes - 1)
                for call in calls:
                        alg.solve(call)
                paths = set()
                for edge in g.edges.values():
                        for path in edge.paths:
                                paths.add(path)
                results += [len(paths)]
        res += [sum(results) / len(results)]
        call_count += [ncalls]
        count += 1
plt.plot(call_count, res)
plt.show()
print(res)

'''
increment = 200
limit = 2000
nodecount = []
res = []
nodes = 0
count = 0
while nodes != limit:
        print(count)
        nodes += increment
        results = []
        for i in range(30):
                graphbldr = Graph_Builder()
                g = graphbldr.build_line(nodes,1)
                calls = gen_call(g, math.ceil(nodes) )
                alg = bga(g, nodes)
                for call in calls:
                        alg.solve(call)
                paths = set()
                for edge in g.edges.values():
                        for path in edge.paths:
                                paths.add(path)
                results += [len(paths)]
        res += [sum(results) / len(results)]
        nodecount += [nodes]
        count += 1
plt.plot(nodecount, res)
plt.show()
print(res)
'''
