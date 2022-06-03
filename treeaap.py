from graph import graph
from aap import online_aap
import random
import math
class treeaap:
    def __init__(self, g):
        self.g = g
        
        aapg = graph()

        self.d = self.find_diameter()

        for node in self.g.nodes:
            aapg.add_node(node)
        for edge in self.g.edges:
            aapg.add_edge(edge[0], edge[1], 2 + math.log(self.d, 2))
        mu = 2**(1+1/1)*self.d
        self.aap = online_aap(aapg, 1, mu, self.d)

    def solve(self, call):
        call.profit = self.d * call.bandwidth
        path = self.aap.solve(call)
        if path == None:
            return None
        edge_used = 0
        for i in range(len(path) - 1):
            edge_used += self.g.get_edge(path[i], path[i+1]).load()
        if edge_used == 0:
            if random.uniform(0, 1) < 1/(4*(1+math.log(self.d, 2))):
                print(path)
                self.accept(path)
    
    def accept(self, path):
        p = self.g.path(path, 1)
        for i in range(len(path) - 1):
            self.g.get_edge(path[i], path[i+1]).paths += [p]




    def find_diameter(self):
        node_number = {}
        node_tagged = {}
        node_queue = []
        in_set = set()
        for node in self.g.nodes:
            if len(self.g.nodes[node].neighbors) == 1:
                node_queue += [ [0,node]]
                in_set.add(node)
            node_number[node] = 0
            node_tagged[node] = 0

        
        while len(node_queue) != 0:
            cur = node_queue.pop(0)
            current_node = cur[1]
            if len(self.g.nodes[current_node].neighbors) - node_tagged[current_node] == 0:
                count_list = []
                for neighbor in self.g.nodes[current_node].neighbors:
                    count_list += [node_number[neighbor]]
                count_list.sort()
                count_list.reverse()
                return count_list[0] + count_list[1]
            number = 0
            for neighbor in self.g.nodes[current_node].neighbors:
                if neighbor in in_set:
                    number = max(number, node_number[neighbor])
            node_number[current_node] = number +1

            for neighbor in self.g.nodes[current_node].neighbors:
                node_tagged[neighbor] += 1
                if neighbor not in in_set:
                    if len(self.g.nodes[neighbor].neighbors) - node_tagged[neighbor] <= 1:
                        number = 0
                        for n in self.g.nodes[neighbor].neighbors:
                            if n in in_set:
                                number = max(number, node_number[n])
                        node_queue += [[number, neighbor]]
                        in_set.add(neighbor)
            
            node_queue.sort()










