from mesh import mesh
from graphbldr import Graph_Builder
import random

def gen_call(g, calls):
    call_list = []
    for i in range(calls):
        samples = random.sample(list(g.nodes), 2)
        print(samples)
        call = g.call(samples[0], samples[1], 1, 1)
        call_list += [call]
    return call_list

n = 40
graphbldr = Graph_Builder()
g = graphbldr.build_mesh(n,n,1)
print(len(g.nodes))
alg = mesh(g)
calls = gen_call(g, 20)
for call in calls:
    alg.solve(call)

paths = set()
for edge in g.edges.values():
    for path in edge.paths:
        paths.add(path)

for path in paths:
    print(path.route)