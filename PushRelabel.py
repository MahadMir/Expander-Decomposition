from AdjacencyList import AdjacencyList
from AdjacencyMatrix import AdjacencyMatrix
import queue
import math
import heapq

class PushRelabel:
    def __init__(self, graph):
        self.graph = graph
        
        self.source = {}
        self.excess = {}
        self.sink = {}
        self.labels = {}
        self.flow_at_vertice = {}
        self.levels = {}

        self.flow = {}
        self.congestion = {}
        self.absorbed = {}

        self.capacity_edge = {}

        self.degree_vector = {}

        self.visited = [0] * self.graph.num_vertices
        
        self.height = 0
        self.capacity = 0
        self.initialized = False
        self.using_2phi_cap = False
        self.already_checked = {}

        self.priority_queue = []


    def set_graph(self, graph):
        self.graph=graph

    def set_source(self, vertices, value):
        for vertex in vertices:
            self.source[vertex] = value

    def set_sink(self, vertices, value):
        for vertex in vertices:
            self.sink[vertex] = value


    def set_using2phi_cap(self, val):
        self.using_2phi_cap = val


    def reset(self):
        self.source = {}
        self.excess = {}
        self.sink = {}
        self.labels = {}
        self.flow_at_vertice = {}
        self.levels = {}

        self.flow = {}
        self.congestion = {}
        self.absorbed = {}

        self.capacity_edge = {}

        self.degree_vector = {}

        self.visited = [0] * self.graph.num_vertices
        
        self.height = 0
        self.capacity = 0
        self.initialized = False
        self.using_2phi_cap = False
        self.already_checked = {}

        self.priority_queue = []


    def add_to_source(self, vertex):
        if vertex in self.source:
            self.source[vertex]+=1
        else:
            self.source[vertex]=1

    def add_to_sink(self, vertex):
        if vertex in self.sink:
            self.sink[vertex]+=1
        else:
            self.sink[vertex]=1
                
    def set_capacity(self, capacity):
        self.capacity = capacity
        self.using_2phi_cap = True

    def set_height(self, height):
        self.height = height

    def initalize_values(self, conductance_wanted, height):
        self.height = height
        self.capacity = 2/conductance_wanted
        self.degree_vector = self.graph.get_degree_vector_dict()

        for i in range((height+1)):
            self.levels[i] = []

        for vertex in self.graph.vertices:
            self.sink[vertex] = self.degree_vector.get(vertex)
            self.flow_at_vertice[vertex] = self.source.get((vertex), 0)
            self.absorbed[vertex] = min(self.sink.get((vertex), 0), self.flow_at_vertice.get((vertex), 0))
            self.excess[vertex] = self.flow_at_vertice.get((vertex), 0) - self.absorbed.get(vertex)
            self.labels[vertex] = 0
            
            if self.excess.get(vertex, 0) > 0:
                self.levels[self.labels.get(vertex, 0)].append(vertex)

        heapq.heappush(self.heap, 0)

        self.initialized = True

    def hot_start(self, flow, labels, source, conductance_wanted, height):
        self.height = height
        self.capacity = 2/conductance_wanted

        self.flow = flow
        self.labels = labels
        self.source = source
        self.degree_vector = self.graph.get_degree_vector_dict()


        if len(self.source.keys) == 0:
            for vertex in self.graph.vertices:
                self.source[vertex] = 0

        for i in range((height+1)):
            self.levels[i] = []

        for vertex in self.labels:
            self.levels[self.labels.get(vertex, 0)].append(vertex)
        
        for vertex in self.graph.vertices:
            self.flow_at_vertice[vertex] = self.source.get(vertex, 0)

        for (u, v) in self.flow:
            self.flow_at_vertice[v]+=self.flow.get((u, v), 0)

        
        for vertex in self.graph.vertices:
            self.sink[vertex] = self.degree_vector.get(vertex)
            self.absorbed[vertex] = min(self.sink.get((vertex), 0), self.flow_at_vertice.get((vertex), 0))
            self.excess[vertex] = self.flow_at_vertice.get((vertex), 0) - self.absorbed.get(vertex)
            

        
        heapq.heappush(self.heap, 0)

        self.initialized = True
        self.using_2phi_cap = True

    
    def smallest_level_in_levels(self):
        curr_min = math.inf
        for i in self.levels:
            if len(self.levels.get(i)) > 0 and i < self.height:
                curr_min = min(curr_min, i)
        return curr_min

    


    def set_congestion(self, congestion):
        self.congestion = congestion

    def UnitFlow(self): 

  

        while self.smallest_level_in_levels() < math.inf and len(self.levels.get(self.smallest_level_in_levels(), 0)) > 0:
            i = self.smallest_level_in_levels()
            vertex = self.levels.get(i, 0)[0]
            self.push_relabel(vertex)

        for vertex in self.graph.vertices:
            for end in self.graph.adjacency_list[vertex]:
                if self.flow.get((vertex, end), 0) > 0:
                    self.congestion[(vertex, end)] = self.congestion.get((vertex, end), 0) + self.flow.get((vertex, end))


        has_excess = {}
        for vertex in self.graph.vertices:
            if self.excess.get(vertex) > 0:
                has_excess[vertex] = True

        return has_excess

    def init_cut_matching_game(self):


        self.degree_vector = self.graph.get_degree_vector_dict()

        for i in range((self.height+1)):
            self.levels[i] = []

        for vertex in self.graph.vertices:
            self.sink[vertex] = self.sink.get(vertex, 0)
            self.flow_at_vertice[vertex] = self.source.get((vertex), 0)
            self.absorbed[vertex] = min(self.sink.get((vertex), 0), self.flow_at_vertice.get((vertex), 0))
            self.excess[vertex] = self.flow_at_vertice.get((vertex), 0) - self.absorbed.get(vertex)
            self.labels[vertex] = 0
            
            if self.excess.get(vertex, 0) > 0:
                self.levels[self.labels.get(vertex, 0)].append(vertex)   




    def get_height(self):
        return self.height

        
    def push_relabel(self, v):
        pushed = False
        for u in self.graph.adjacency_list[v]:
            if self.using_2phi_cap:
                if self.capacity_edge.get((v, u), self.capacity) - self.flow.get((v, u), 0) > 0 and \
                self.labels.get(v) == self.labels.get(u) + 1 and not self.already_checked.get((v, u), False):  #first line is residual capacity
                    self.push(v, u)
                    self.already_checked[(v, u)] = True
                    pushed = True
                    break
        if not pushed:
            self.relabel(v)


    def push(self, v, u):
        assert self.excess.get(u) == 0


        tau = min(self.excess.get(v), min(self.capacity_edge.get((v, u), self.capacity) - self.flow.get((v, u), 0), self.degree_vector.get(u) - self.excess.get(u)))

        self.flow[(v, u)] = self.flow.get((v, u), 0) + tau
        self.flow[(u, v)] = self.flow.get((u, v), 0) - tau

        self.flow_at_vertice[v] -= tau
        

        self.absorbed[v] = min(self.flow_at_vertice.get(v), self.sink.get(v))
        self.excess[v] = self.flow_at_vertice.get(v) - self.absorbed[v] 
        if self.excess.get(v) == 0:
            self.levels[self.labels.get(v)].remove(v)
        
        
        self.flow_at_vertice[u] += self.flow.get((v, u))
        self.absorbed[u] = min(self.flow_at_vertice.get(u), self.sink.get(u))
        self.excess[u] = self.flow_at_vertice.get(u) - self.absorbed[u]

        if self.excess.get(u) > 0:
            self.levels[self.labels.get(u)].append(u)





    def relabel_assert(self, v):
        all_vertices_labels_smaller = False
        for u in self.graph.vertices:
            if (v, u) in self.capacity_edge and self.capacity_edge.get((v, u), self.capacity) - self.flow.get((v, u), 0) > 0:
                assert self.labels.get(v) <= self.labels.get(u), f"{v} {u} {self.graph.adjacency_list[v]} {self.labels[v]} {self.height}"



    def relabel(self, v):
        assert self.labels.get(v) < self.height and self.excess.get(v) > 0
        self.relabel_assert(v)
        self.labels[v] = self.labels.get(v) + 1
        self.levels[self.labels.get(v)].append(v)
        self.levels[self.labels.get(v)-1].remove(v)
        
        for u in self.graph.adjacency_list[v]:
            self.already_checked[(v, u)] = False
            

    def level_cut(self, h):
        cut_levels = {}
        for i in range((h+1)):
            cut_levels[i] = []

        for vertex in self.graph.vertices:
            cut_levels[self.labels.get(vertex, 0)].append(vertex)

        volume = 0
        best_conductance = 1.0
        best_level = h

        for level in range(h, 0, -1):
            z = 0
            for u in cut_levels[level]:
                volume += self.degree_vector[u]
                for v in self.graph.adjacency_list[u]:
                    if self.labels[u] == self.labels[v] + 1:
                        z += 1
            conductance = z / min(volume, self.graph.get_volume() - volume)
            if conductance < best_conductance:
                best_conductance = conductance
                best_level = level

        left, right = [], []
        for level in range(h, best_level - 1, -1):
            left.extend(cut_levels[level])
        for level in range(0, best_level):
            right.extend(cut_levels[level])

        return left, right 
    

    def has_excess(self):
        l = []
        for vert in self.graph.adjacency_list:
            if self.labels[vert] >= self.height:
                l.append(vert)

        return l

    def matching_dfs(self, sources):
        matches = []

        def search(start):
            path = []

            def dfs(u):
                self.visited[u] = start + 1

                if self.absorbed[u] > 0 and self.sink[u] > 0:
                    self.absorbed[u] -= 1
                    self.sink[u] -= 1
                    return u

                for v in self.graph.adjacency_list[u]:
                    if self.flow.get((u,v), 0) <= 0 or self.visited[v] == start + 1:
                        continue

                    path.append((u, v))
                    m = dfs(v)
                    if m != -1:
                        return m
                    path.pop()

                return -1

            m = dfs(start)
            if m != -1:
                for e in path:
                    self.flow[(e)] = self.flow.get(e, 0) - 1
            return m

        for u in sources:
            m = search(u)
            if m != -1:
                matches.append((u, m))

        for u in self.graph.vertices:
            self.visited[u] = False

        return matches