from graph import graph

class online_aap:
    def __init__(self, g, epsilon, mu, D):
        self.g = g
        #self.D = len(g.nodes)
        self.D = D
        #epsilon between 0 and 1
        self.epsilon = epsilon
        #self.mu = 2^(1+1/self.epsilon)*self.D
        self.mu = mu
    

    def solve(self, call):
        path = self.route(call)
        if path == None:
            #print("No valid path\n")
            return None
        gpath = self.g.path(path, call.bandwidth)
        for i in range(0, len(path) - 1):
            edge = self.g.get_edge(path[i], path[i+1])
            edge.paths += [gpath]
        #print("Accepted path\n")
        #print(path)
        return path        

        
    def route(self, call):
        vertex_set = {}
        for id in self.g.nodes:
            vertex_set[id] = None
        
        node_queue = [call.start]

        #tuple contains current sum of load from the incoming edge in the first position, and id of parent in second position.
        vertex_set[call.start] = (0, None)

        while len(node_queue) > 0:
            current_node = node_queue.pop(0)
            neighbors = self.g.nodes[current_node].neighbors
            for neighbor in neighbors:
                if vertex_set[neighbor] != None:
                    continue
                edge = self.g.get_edge(current_node, neighbor)
                if call.bandwidth <= edge.capacity-edge.load():
                    edge_cost_func = edge.capacity*(self.mu**(1/edge.capacity * edge.load()) - 1)
                    cost = (call.bandwidth/edge.capacity) * edge_cost_func + vertex_set[call.start][0]
                    if cost <= call.profit:
                        vertex_set[neighbor] = (cost, current_node)
                        if neighbor == call.end:
                            break
                        node_queue += [neighbor]
            if vertex_set[call.end] != None:
                break
            
        if vertex_set[call.end] != None:
            current = call.end
            path = []
            while current != None:
                path = [current] + path
                current = vertex_set[current][1]
            return path
        else:
            #print("no valid path\n")
            return None






