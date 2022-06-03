class graph:
    def __init__(self):
        self.edges = {}
        self.nodes = {}
    
    def add_node(self, id):
        if id not in self.nodes:
            new_node = self.node(id)
            self.nodes[id] = new_node
        else:
            print("node already exists/n")
    
    def add_edge(self, id1, id2, capacity):
        if id1 == id2:
            print("same node \n")
            return
        if id1 < id2:
            first = id1
            second = id2
        else:
            first = id2
            second = id1
        
        if (first, second) not in self.edges:
            new_edge = self.edge(first, second, capacity)
            self.edges[(first, second)] = new_edge
            self.nodes[id1].neighbors += [id2]
            self.nodes[id2].neighbors += [id1]
        else:
            print("edge already exists/n")

    def get_edge(self, id1, id2):
        if id1 < id2:
            first = id1
            second = id2
        else:
            first = id2
            second = id1
        
        edge = self.edges[(first, second)]
        return edge

    def get_node(self, id1):
        node = self.nodes[id1]
        if node == None:
            print("No node with that id\n")
            return None
        return node

    class node:
        def __init__(self, id):
            self.neighbors = []
            self.id = id 

    class edge:
        def __init__(self, id1, id2, capacity):
            if id1 < id2:
                self.pair = (id1, id2)
            else:
                self.pair = (id2, id1)
            self.paths = []
            self.capacity = capacity
            
        def load(self):
            usage = 0
            for path in self.paths:
                usage += path.bandwidth
            return usage

    class path:
        def __init__(self, route, bandwidth):
            self.route = route
            self.bandwidth = bandwidth


    class call:
        def __init__(self, start, end, bandwidth, profit):
            self.start = start
            self.end = end
            self.bandwidth = bandwidth
            self.profit = profit


    