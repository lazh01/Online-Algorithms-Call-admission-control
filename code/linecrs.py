from graph import graph
import math
import random

class linecrs:
    def __init__(self, g):
        self.g = g
        self.edge_rank = {}
        for node in self.g.nodes:
            if len(g.get_node(node).neighbors) == 1:
                current_node = node
                break

        line = []
        neighbor = g.get_node(current_node).neighbors[0]
        edge = g.get_edge(neighbor, current_node)
        while edge != None:
            line += [edge]
            last_node = current_node
            current_node = neighbor
            if len(g.nodes[current_node].neighbors) > 1:
                if g.nodes[current_node].neighbors[0] != last_node:
                    neighbor = current_node.neighbors[0]
                    edge = self.g.get_edge(current_node, neighbor)
                else:
                    neighbor = g.nodes[current_node].neighbors[1]
                    edge = self.g.get_edge(current_node, neighbor)
            else:
                edge = None
        
        self.rank(line, 0)
        #for edge in line:
        #    print(self.edge_rank[edge])
        self.r_level = random.randint(0, math.ceil(math.log(len(self.g.edges), 2)))
        #print(self.r_level)

    def rank(self, line, level):
        
        if len(line) == 0:
            return
        index = math.ceil(len(line)/2)-1
        self.edge_rank[line[index]] = level
        self.rank(line[0:index], level + 1)
        self.rank(line[index + 1: len(line)], level + 1)
    
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
        index = 0
        level = math.ceil(math.log(len(self.g.edges)))
        while index != len(route) - 1:
            edge = self.g.get_edge(route[index], route[index+1])
            if self.edge_rank[edge] < level:
                level = self.edge_rank[edge]
            index += 1
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
