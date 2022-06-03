from graph import graph
import math
class bga:
    def __init__(self, g, R):
        self.L = 2*R
        self.g = g

    def solve(self, call):
        path = self.route(call)
        if path == None:
            return
        else:
            self.accept(path, call.bandwidth)
    
    def route(self, call):
        vertex_set = {}
        for id in self.g.nodes:
            vertex_set[id] = None

        dist = {}
        for id in self.g.nodes:
            dist[id] = math.inf
        
        node_queue = [call.start]
        dist[call.start] = 0

        while len(node_queue) > 0:
            current_node = node_queue.pop(0)
            if dist[current_node] == self.L:
                continue
            neighbors = self.g.nodes[current_node].neighbors
            for neighbor in neighbors:
                if vertex_set[neighbor] != None or neighbor == call.start:
                    continue
                edge = self.g.get_edge(current_node, neighbor)
                if edge.load() == 0:
                    vertex_set[neighbor] = current_node
                    dist[neighbor] = dist[current_node] + 1
                    node_queue += [neighbor] 
            if vertex_set[call.end] != None:
                break
            
        if vertex_set[call.end] != None:
            current = call.end
            path = []
            while current != None:
                path = [current] + path
                current = vertex_set[current]
            return path
        else:
            #print("no valid path\n")
            return None


    def accept(self, path, bandwidth):
        t_path = self.g.path(path, bandwidth)
        index = 0
        while index != len(path)  - 1:
            edge = self.g.get_edge(path[index], path[index + 1])
            edge.paths += [t_path]
            index += 1
