from graph import graph
import math
import random

class treecrs:
    def __init__(self, g):
        self.g = g
        self.node_rank = {}
        self.levels = 0
        node_set = set()
        for node in g.nodes:
            node_set.add(node)

        self.rankq = [[node_set, 0]]
        while len(self.rankq) != 0:
            current = self.rankq.pop(0)
            self.rank(current[0], current[1])
        #print(self.levels)
        self.r_level = random.randint(0, self.levels)
        #print(self.levels)
        #print(self.r_level)
        #print(self.node_rank)
        #print(len(self.node_rank))
        #for node in self.g.nodes:
        #    print(node)
        #    print(self.node_rank[node])
        #for edge in line:
        #    print(self.edge_rank[edge])
        #self.r_level = random.randint(0, math.ceil(math.log(len(self.g.edges), 2)))
        #print(self.r_level)

    def rank(self, node_set, level):
        
        if len(node_set) == 0:
            return
        node_number = {}
        for node in node_set:
            node_number[node] = 0

        node_tagged = {}
        for node in node_set:
            node_tagged[node] = 0
            
        node_queue = []
        for node in node_set:
            count = 0
            for neighbor in self.g.get_node(node).neighbors:
                if neighbor in node_set:
                    count += 1
            if count == 1:
                node_queue += [[0, node]]

        while len(node_queue) != 0:
            cur = node_queue.pop(0)
            current_node = cur[1]
            if node_number[current_node] > 0:
                continue
            node_number[current_node] = cur[0] + 1
            for neighbor in self.g.get_node(current_node).neighbors:
                if neighbor not in node_set:
                    continue
                if node_number[neighbor] > 0:
                    continue
                
                if node_number[neighbor] == 0:
                    node_tagged[neighbor] += 1
                if len(self.g.nodes[neighbor].neighbors) - node_tagged[neighbor] <= 1:
                    time = 0
                    for n in self.g.nodes[neighbor].neighbors:
                        if n not in node_set:
                            continue
                        time += node_number[n]
                    node_queue += [[time, neighbor]]
            
            node_queue.sort()
            

        middle = max(node_number, key = node_number.get)
        self.node_rank[middle] = level
        node_set.remove(middle)


        for neighbor in self.g.nodes[middle].neighbors:
            if neighbor not in node_set:
                continue
            n_set = set()
            node_queue = [neighbor]
            n_set.add(neighbor)
            while len(node_queue) != 0:
                current_node = node_queue.pop(0)
                for n in self.g.nodes[current_node].neighbors:
                    if n not in node_set:
                        continue
                    if n in n_set:
                        continue
                    n_set.add(n)
                    node_queue += [n]
            #print(len(n_set))
            self.rankq += [[n_set, level + 1]]
        
        self.levels = max(self.levels, level)
    
    def solve(self, call):
        path = self.route(call)
        if path == None:
            return
        level = self.path_level(path)
        if level == self.r_level:
            self.accept(path, call.bandwidth)

    def accept(self, path, bandwidth):
        t_path = self.g.path(path, bandwidth)
        index = 0
        while index != len(path)  - 1:
            edge = self.g.get_edge(path[index], path[index + 1])
            edge.paths += [t_path]
            index += 1


    def path_level(self, route):
        level = math.inf
        for node in route:
            level = min(level, self.node_rank[node])
        return level

    def route(self, call):
        vertex_set = {}
        for id in self.g.nodes:
            vertex_set[id] = None
        
        node_queue = [call.start]

        vertex_set[call.start] = call.start

        while len(node_queue) > 0:
            current_node = node_queue.pop(0)
            neighbors = self.g.nodes[current_node].neighbors
            for neighbor in neighbors:
                if vertex_set[neighbor] != None:
                    continue
                edge = self.g.get_edge(current_node, neighbor)
                if call.bandwidth <= edge.capacity - edge.load():
                    vertex_set[neighbor] = current_node
                    node_queue += [neighbor]
        
        if vertex_set[call.end] != None:
            current = call.end
            path = []
            while current != call.start:
                path = [current] + path
                current = vertex_set[current]
            path = [current] + path
            return path
        else:
            #print("no valid path\n")
            return None