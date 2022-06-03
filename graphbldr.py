from graph import graph
import random

class Graph_Builder:
    def build_line(self, n, c):
        g = graph()
        for i in range(1,n+1):
            g.add_node(i)
            if i > 1:
                g.add_edge(i-1,i, c)

        return g
    
    def build_tree(self, n, c):
        g = graph()
        
        free_nodes = set()
        for i in range(1,n+1):
            g.add_node(i)
            free_nodes.add(i)
        
        in_tree = set()
        clist = random.sample(free_nodes, 1)
        cnode = clist[0]
        in_tree.add(cnode)
        free_nodes.remove(cnode)

        while len(free_nodes) != 0:
            a_node = random.sample(free_nodes, 1)[0]
            b_node = random.sample(in_tree, 1)[0]
            g.add_edge(a_node, b_node, c)
            in_tree.add(a_node)
            free_nodes.remove(a_node)
        
        return g
    
    
    def build_mesh(self, n, m, c):
        n_count = 0
        g = graph()

        arrx = []
        for x in range(n):
            arry = []
            for y in range(m):
                n_count += 1
                arry += [n_count]
                g.add_node(n_count)
            arrx += [arry]
        
        for x in range(n):
            for y in range(m):
                if x > 0:
                    g.add_edge(arrx[x][y], arrx[x-1][y], c)
                if y > 0:
                    g.add_edge(arrx[x][y], arrx[x][y-1], c)
        
        return g
    

        

