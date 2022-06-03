import graph
import math
import random
import aap

class mesh:
    def __init__(self, graph):
        self.graph = graph
        
        c = 1 #need adjust
        p = 1 #need adjust
        self.block_width = math.floor(c * math.log(len(self.graph.nodes), 2))
        self.long_cap = math.ceil(p * math.log(len(self.graph.nodes), 2))
        self.node_to_mesh_pos = {}
        corners = self.find_corners()
        self.mesh = self.gen_mesh(corners)
        self.long_struct = self.longGraph(4)
        self.mode = random.randint(1,2)

    
    def solve(self, call):
        if self.mode == True:
            return self.long_struct.solve(call)
        if self.mode == 2:
            return



    def short(self):
        return



    def mis(self, graph):
        node_set = set()
        nodesval = {}
        for node_id in graph.nodes:
            node_set.add(node_id)
        ind_set = set()
        
        while(len(node_set) > 0):
            for node_id in node_set:
                nodesval[node_id] = random.random()
            for node_id in node_set:
                ismax = True
                for neighbor in graph.nodes[node_id].neighbors:
                    if neighbor in node_set:
                        if nodesval[neighbor] > nodesval[node_id]:
                            ismax = False
                if ismax == True:
                    ind_set.add(node_id)

            for node_id in ind_set:
                node_set.remove(node_id)
                for neighbor in graph.nodes[node_id].neighbors:
                    node_set.remove(neighbor)
        
        return ind_set

    def longGraph(self, neighborhood):
        width = len(self.mesh)
        height = len(self.mesh[0])

        centers = []
        print(math.floor(width/self.block_width))
        for x in range(math.floor(width/self.block_width)):
            column = []
            for y in range(math.floor(height/self.block_width)):
                block = self.block(math.ceil(x * self.block_width) - math.floor(0.5 * self.block_width), math.ceil(y * self.block_width) - math.floor(0.5 * self.block_width), self.block_width)
                column += [block]
            centers += [column]

        center_graph = graph.graph()
        self.graph_to_index = {}
        self.index_to_graph = {}
        node_id  = 0
        for x in range(len(centers)):
            for y in range(len(centers[0])):
                center_graph.add_node(node_id)
                centers[x][y].node_id = node_id
                self.graph_to_index[node_id] = (x,y)
                self.index_to_graph[(x,y)] = node_id
                for y_dist in range(1,neighborhood+1):
                    for x_dist in range(1,neighborhood+1):
                        if (x_dist + y_dist > neighborhood) or (x - x_dist < 0) or (y - y_dist < 0) :
                            continue
                        center_graph.add_edge(node_id, self.index_to_graph[(x - x_dist, y - y_dist)], 1)
                node_id += 1

        ind_set = mis(center_graph)

        #assign 8 surrounding blocks to block in ind_set
        for node_id in ind_set:
            index = self.graph_to_index[node_id]
            for x in range(-1,2):
                for y in range(-1,2):
                    if index[0] + x < 0 or index[0] + x > len(centers) - 1 or index[1] + y < 0 or index[1] + y > len(centers[0]) -1:
                        continue
                    centers[index[0] + x][index[1] + y].cluster = centers[index[0]][index[1]]
        
        #determine which cluster each blocks neighbor is a part of
        for x in range(len(centers)):
            for y in range(len(centers[0])):
                if centers[x][y].cluster != None:
                    if x + 1 < len(centers):
                        centers[x+1][y].west = centers[x][y].cluster
                    if x - 1 >= 0:
                        centers[x-1][y].east = centers[x][y].cluster
                    if y + 1 < len(centers[0]):
                        centers[x][y+1].north = centers[x][y].cluster
                    if y - 1  >= 0:
                        centers[x][y-1].south = centers[x][y].cluster
        
        #for each block not assigned a cluster, choose a cluster from neighbors determined in previous step
        for x in range(len(centers)):
            for y in range(len(centers[0])):
                if centers[x][y].cluster == None:
                    cluster_cand = set()
                    if centers[x][y].north != None:
                        cluster_cand.add(centers[x][y].north)
                    if centers[x][y].west != None:
                        cluster_cand.add(centers[x][y].west)
                    if centers[x][y].east != None:
                        cluster_cand.add(centers[x][y].east)
                    if centers[x][y].south != None:
                        cluster_cand.add(centers[x][y].south)
                    candidates = list(cluster_cand)
                    if len(candidates) > 0:
                        centers[x][y].cluster = random.sample(candidates,1)[0]
        
        #determine which cluster each blocks neighbor is a part of again, now that all blocks have clusters
        for x in range(len(centers)):
            for y in range(len(centers[0])):
                    if x + 1 < len(centers):
                        centers[x+1][y].west = centers[x][y].cluster
                    if x - 1 >= 0:
                        centers[x-1][y].east = centers[x][y].cluster
                    if y + 1 < len(centers[0]):
                        centers[x][y+1].north = centers[x][y].cluster
                    if y - 1  >= 0:
                        centers[x][y-1].south = centers[x][y].cluster
        

        #create graph from  clusters with p log n capacity edges between neighboring clusters
        long_sim_graph = graph.graph()
        print(ind_set)
        for node_id in ind_set:
            long_sim_graph.add_node(node_id)
        for x in range(len(centers)):
            for y in range(len(centers[0])):
                print(x)
                print(y)
                if centers[x][y].south != centers[x][y].cluster and centers[x][y].south != None:
                    long_sim_graph.add_edge(centers[x][y].south.node_id, centers[x][y].cluster.node_id, self.long_cap)
                if centers[x][y].north != centers[x][y].cluster and centers[x][y].north != None:
                    long_sim_graph.add_edge(centers[x][y].north.node_id, centers[x][y].cluster.node_id, self.long_cap)
                if centers[x][y].east != centers[x][y].cluster and centers[x][y].east != None:
                    long_sim_graph.add_edge(centers[x][y].east.node_id, centers[x][y].cluster.node_id, self.long_cap)
                if centers[x][y].west != centers[x][y].cluster and centers[x][y].west != None:
                    long_sim_graph.add_edge(centers[x][y].west.node_id, centers[x][y].cluster.node_id, self.long_cap)

        return self.long_graph(long_sim_graph, centers, self.graph_to_index, self.index_to_graph, ind_set, self.mesh, self.node_to_mesh_pos, self.block_width )

        
    class long_graph:
        def __init__(self, sim_graph, block_array, graph_to_index, index_to_graph, ind_set, mesh, node_to_mesh_pos, block_width):
            self.block_array = block_array
            self.sim_graph = aap.online_aap(sim_graph, 1, 2**(1+1/1)*(len(mesh) - 1 + len(mesh[0]) -1), 2**(1+1/1)*(len(mesh) - 1 + len(mesh[0]) -1))
            self.graph_to_index = graph_to_index
            self.index_to_graph = index_to_graph
            self.call_center_set = ind_set
            self.mesh = mesh
            self.node_to_mesh_pos = node_to_mesh_pos
            self.block_width = block_width



        def solve(self, call):
            start_pos = self.node_to_mesh_pos[call.start]
            end_pos = self.node_to_mesh_pos[call.end]
            start_block = self.get_block(start_pos[0], start_pos[1])
            end_block = self.get_block(end_pos[0], end_pos[1])
            
            
            if start_block.node_id not in self.call_center_set:
                print("Start not in call center\n")
                return None

            if end_block.node_id not in self.call_center_set:
                print("End not in call center\n")
                return None
            
            print(self.call_center_set)
            print(start_block.node_id)
            start_node = self.sim_graph.g.get_node(start_block.node_id)
            total_load = 0
            for neighbor in start_node.neighbors:
                edge = self.sim_graph.g.get_edge(start_node.id, neighbor)
                total_load += edge.load()
            if total_load % 2 != 0:
                print("Start block already used\n")
                return None
            
            end_node = self.sim_graph.g.get_node(end_block.node_id)
            total_load = 0
            for neighbor in end_node.neighbors:
                edge = self.sim_graph.g.get_edge(end_node.id, neighbor)
                total_load += edge.load()
            if total_load % 2 != 0:
                print("End block already used\n")
                return None

            cals = self.sim_graph.g.call(start_block.node_id, end_block.node_id, 1, 1)
            cluster_path = self.sim_graph.solve(cals)


        def get_block(self, x, y):
            block_x = math.floor(x / self.block_width)
            block_y = math.floor(y / self.block_width)
            return self.block_array[block_x][block_y]
        




    class block:
        def __init__(self, x, y, blockwidth):
            self.center = (x,y)
            self.north = None
            self.west = None
            self.east = None
            self.south = None
            self.cluster = None
            self.node_id = None
            self.blockwidth = blockwidth


    def gen_mesh(self, corners):
        """
        node_queue = [corners[0]]
        dist= {}

        for n in self.graph.nodes:
            dist[n] = math.inf
        
        dist[node_queue[0]] = 0

        while len(node_queue) > 0:
            current_node = self.graph.nodes[node_queue.pop()]

            for node in current_node.neighbors:
                if dist[node] > dist[current_node.id] + 1:
                    dist[node] = dist[current_node.id] + 1
                    node_queue += [node]
        
        """

        dist1 = self.get_distance_n(corners[0])

        corner_dist = []
        for n in corners:
            corner_dist += [(dist1[n], n)]

        corner_dist.sort()

        w = corner_dist[1][0]
        h = corner_dist[2][0]

        mesh = [[0 for x in range(h + 1 )] for y in range(w + 1)]

        mesh[0][0] = corner_dist[0][1]
        mesh[w-1][0] = corner_dist[1][1]
        mesh[0][h-1] = corner_dist[2][1]
        mesh[w-1][h-1] = corner_dist[3][1]

        

        dist2 = self.get_distance_n(corner_dist[1][1])

        for node in self.graph.nodes:
            for x in range(w+1):
                if dist1[node] - x == dist2[node] - (w - x):
                    mesh[x][dist1[node] - x] = node
                    self.node_to_mesh_pos[node] = (x, dist1[node] - x)
        
        return mesh

    def get_distance_n(self, n):
        node_queue = [n]
        dist= {}

        for n in self.graph.nodes:
            dist[n] = math.inf
        
        dist[node_queue[0]] = 0

        while len(node_queue) > 0:
            current_node = self.graph.nodes[node_queue.pop()]

            for node in current_node.neighbors:
                if dist[node] > dist[current_node.id] + 1:
                    dist[node] = dist[current_node.id] + 1
                    node_queue += [node]
        
        return dist




    def find_corners(self):
        corners = []
        for node in self.graph.nodes:
            if len(self.graph.nodes[node].neighbors) == 2:
                corners += [node]
        return corners

def mis(graph):
        node_set = set()
        nodesval = {}
        for node_id in graph.nodes:
            node_set.add(node_id)
        ind_set = set()
        
        while(len(node_set) > 0):
            for node_id in node_set:
                nodesval[node_id] = random.random()

            for node_id in node_set:
                ismax = True
                for neighbor in graph.nodes[node_id].neighbors:
                    if neighbor in node_set:
                        if nodesval[neighbor] > nodesval[node_id]:
                            ismax = False
                if ismax == True:
                    ind_set.add(node_id)

            for node_id in ind_set:
                if node_id in node_set:
                    node_set.remove(node_id)
                for neighbor in graph.nodes[node_id].neighbors:
                    if neighbor in node_set:
                        node_set.remove(neighbor)
        
        return ind_set