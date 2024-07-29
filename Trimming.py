from PushRelabel import PushRelabel
import math

class Trimming:
    def __init__(self, graph, small_vol_cut, conductance):
        self.graph = graph
        self.small_vol_cut = small_vol_cut
        self.conductance = conductance

        self.current_set = set(small_vol_cut)
        self.other_set = set(self.graph.vertices) - self.current_set

   
    def calculate_source_per_vertex(self, vertex, right_set):
        count = 0
        for vert in right_set:
            if vert in self.graph.adjacency_list[vertex]:
                count+=1
        return count



    def calculate_volume(self, vertices):
        if len(vertices) == 0:
            return 0
        else:
            vol = 0
            for vertice in vertices:
                vol+=self.graph[vertice]
            return vol


    def make_new_flow_dict(self, flow):
        new_flow_dict = {}
        for x in list(self.current_set):
            for y in list(self.current_set):
                if (x, y) in flow:
                    new_flow_dict[(x, y)] = flow[(x,y)]


    def make_new_labels_dict(self, labels):
        new_label_dict = {}
        for x in list(self.current_set):
            if x in labels:
                new_label_dict[x] = labels[x]

    def compute(self):
        flow = {}
        height = (40 + math.log(2*self.graph.num_edges)/self.conductance)
        labels = {}
        source = {}

        for vertex in self.current_set:
            current_size = self.calculate_source_per_vertex(vertex, self.other_set)
            source[vertex] = source.get(vertex, 0) + (2/self.conductance)*current_size


        while True:
            induced_graph = self.graph.degree_preserving_induced_subgraph(list(self.current_set))
            flow_problem = PushRelabel(induced_graph)
            flow_problem.reset()
            flow_problem.hot_start(flow, labels, source, self.conductance, height)
            has_excess = flow_problem.UnitFlow()
            if (len(has_excess)<=0):
                break
            left, right = flow_problem.level_cut(height)
            min_cut = []
            if self.calculate_volume(left) <= self.calculate_volume(right):
                min_cut = left
            else:
                min_cut = right
            
            if len(min_cut)<=0:
                break
            
            min_cut = set(min_cut)
            self.current_set = self.current_set - min_cut
            self.other_set = set(self.graph.vertices) - self.current_set

            flow = self.make_new_flow_dict(flow_problem.flow)
            labels = self.make_new_labels_dict(flow_problem.labels)
            for vertex in self.current_set:
                source[vertex] += (2/self.conductance)*self.calculate_source_per_vertex(vertex, min_cut)

        return self.current_set
