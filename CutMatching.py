import math
import numpy as np
from PushRelabel import PushRelabel
from AdjacencyList import AdjacencyList
import time

class CutMatching():

    def __init__(self, graph, conductance, t1, t2):
        
        self.graph = graph
        self.subdivision_graph = graph.make_subdivision_graph()
        self.subdivision_graph_degree_vector = self.subdivision_graph.get_degree_vector_dict()
        self.conductance = conductance
        self.t1 = t1
        self.t2 = t2

        self.subdivision_edges = self.subdivision_graph.num_edges


        self.flow_matrix = np.identity(self.subdivision_graph.num_vertices)


        self.A = set(self.subdivision_graph.vertices) 
        self.R = set()
        self.X = set(self.subdivision_graph.make_subdivision_verts)

    def cut_matching(self):

        big_t = math.ceil(self.t1 + self.t2*math.log2(self.subdivision_graph.num_edges))
        small_t = 1
        c = math.ceil(1/(self.conductance*big_t))
        self.congestion = {}

        for u in self.subdivision_graph.vertices:
            for v in self.subdivision_graph.adjacency_list[u]:
                self.congestion[(u, v)] = 0
                self.subdivision_graph.capacity[(u, v)] = c  


        i = 1
        current_flow_subgraph = self.subdivision_graph

        while small_t <= big_t and self.calculate_volume(self.R) <= self.subdivision_edges/(10*big_t):

            print("Current Iteration: ", (i, big_t))
            small_t+=1
            print("Cut Player Starting")
            c_t = time.time()
            source, target = self.make_cut()
            print("Cut Player Ending ")
            print(f"Cut found in {time.time()-c_t} seconds")
            unit_flow = PushRelabel(current_flow_subgraph)      
            unit_flow.reset()
            unit_flow.set_congestion(self.congestion)
            for s in source:
                unit_flow.add_to_source(s)
            for t in target:
                unit_flow.add_to_sink(t)
            unit_flow.set_capacity(int(math.ceil(1/self.conductance/(math.log10(current_flow_subgraph.num_edges)**2))))
            unit_flow.set_height(int(math.ceil(1/self.conductance/math.log10(current_flow_subgraph.num_edges))))
            unit_flow.init_cut_matching_game()

            c_t = time.time()
            print("Flow Player Starting")
            has_excess = unit_flow.UnitFlow()
            print("Flow Player Ending ")
            print(f"Flow found in {time.time()-c_t} seconds")


            cut_found = set()
            matching = []
            valid_sources = source
            if len(has_excess) > 0:
                print("excess found")
                self.cut_found = True

                print("making level cut")
                left_cut, right_cut = unit_flow.level_cut(unit_flow.height)
                print("level cut found")

                min_vol_cut = left_cut if current_flow_subgraph.get_volume_vertices(left_cut) < current_flow_subgraph.get_volume_vertices(right_cut) else right_cut
                min_vol_cut = set(min_vol_cut)
                cut_found = min_vol_cut


                valid_sources = source - min_vol_cut
                
                unit_flow = PushRelabel(current_flow_subgraph)      
                unit_flow.reset()
                unit_flow.set_congestion(self.congestion)
                for s in valid_sources:
                    unit_flow.add_to_source(s)
                for t in target:
                    unit_flow.add_to_sink(t)
                unit_flow.set_capacity(int(math.ceil(1/self.conductance/(math.log10(current_flow_subgraph.num_edges)**2))))
                unit_flow.set_height(int(math.ceil(1/self.conductance/math.log10(current_flow_subgraph.num_edges))))
                unit_flow.init_cut_matching_game()
                c_t = time.time()
                print("Flow Player Redoing with New Vertices")
                has_excess = unit_flow.UnitFlow()
                print("Flow Player Ending ")
                print(f"Flow found in {time.time()-c_t} seconds")
                if len(has_excess) > 0:
                    print("height is probably one", unit_flow.height)

            print("Matching Started")
            matching = unit_flow.matching_dfs(list(valid_sources))
            print("Matching Ended")

            print("Flow Matrix Update Starting")
            for match in matching:
                x,y = match
                self.flow_matrix[x] = self.flow_matrix[x]/2 + self.flow_matrix[y]/2
            print("Flow Matrix Update Ending")


            if len(cut_found) > 0:
                self.A = self.A - cut_found
                self.R = self.R.union(cut_found)
                current_flow_subgraph = self.subdivision_graph.degree_preserving_induced_subgraph(list(self.A))


            i+=1
            



        if self.calculate_volume(self.R) >= self.subdivision_edges/(10*big_t):
            return (self.A & set(self.graph.vertices), self.R & set(self.graph.vertices), 1)
        elif self.subdivision_graph.num_vertices == 0:
            return (self.A & set(self.graph.vertices), self.R & set(self.graph.vertices), 0)
        elif len(self.R) == 0:
            return (self.A & set(self.graph.vertices), self.R & set(self.graph.vertices), 0)
        else:
            return (self.A & set(self.graph.vertices), self.R & set(self.graph.vertices), -1)


                        
    def get_avg_flow_vector(self):

        zero_vec = np.zeros(self.flow_matrix.shape[0])
        subdivision_verts_in_A = list(self.A.intersection(self.X))
        length = len(subdivision_verts_in_A)
        i = 0
        for subdiv_vert in subdivision_verts_in_A:
            zero_vec += self.flow_matrix[subdiv_vert]
        zero_vec/=length
        return zero_vec

    def make_cut(self):
        avg_flow = self.get_avg_flow_vector()
        dim = avg_flow.shape[0]
        ortho_one = self.orthogonal_to_all_ones(dim)
        avg_proj_flow = np.dot(avg_flow, ortho_one)

        ax_left = []
        ax_right = []

        source_set = set()
        target_set = set()

        subdivision_verts_in_A = list(self.A.intersection(self.X))


        for vertex in subdivision_verts_in_A:
            proj_ver = np.dot(ortho_one, self.flow_matrix[vertex])
            print(proj_ver)
            if proj_ver < avg_proj_flow:
                ax_left.append((vertex, proj_ver))
            else:
                ax_right.append((vertex, proj_ver))
            
        if len(ax_left) > len(ax_right):
            ax_left, ax_right = ax_right, ax_left

        if self.compute_potential([x for x, y in ax_left], ortho_one, avg_proj_flow) > (1/20) * self.compute_potential(subdivision_verts_in_A, ortho_one, avg_proj_flow):
            
            ax_left_sorted = sorted(ax_left, key=lambda x: x[1])
            ax_left = [x for x,y in ax_left_sorted]

            while len(ax_left)*8 > len(subdivision_verts_in_A):
                ax_left.pop()

            ax_right_sorted = sorted(ax_right, key=lambda x: x[1])
            ax_right = [x for x,y in ax_right_sorted]

            source_set.update(ax_left)
            target_set.update(ax_right)

        else:
            separation_val = 0
            for vertex, projection in ax_left:
                separation_val+=abs(projection-avg_proj_flow)
            

            diff = separation_val
            separation_val/=len(subdivision_verts_in_A)
            separation_val*=4
            separation_val+=avg_proj_flow

            a_target = []
            a_r = []
            for subdiv_vert in subdivision_verts_in_A:
                proj = np.dot(self.flow_matrix[subdiv_vert], ortho_one)
                if  proj <= separation_val:
                    a_target.append(subdiv_vert)
                elif proj >= avg_proj_flow + (6*diff)/len(subdivision_verts_in_A):
                    a_r.append((subdiv_vert, proj))

            a_r = sorted(ax_left, key=lambda x: x[1], reverse=True)

            while len(a_r)*8 > len(subdivision_verts_in_A):
                a_r.pop() 

            a_r = [x for x,y in a_r]


            target_set.update(a_target)
            source_set.update(a_r)

  
        return (source_set, target_set)
        
        

    def compute_potential(self, vertex_set, ortho_vec, avg_proj_flow):

        potential = 0
        for vertex in vertex_set:
            potential+= abs(np.dot(self.flow_matrix[vertex], ortho_vec) - avg_proj_flow)**2
        return potential


    def calculate_volume(self, vertices):
        if len(vertices) == 0:
            return 0
        else:
            vol = 0
            for vertice in vertices:
                vol+=self.subdivision_graph_degree_vector[vertice]
            return vol



    def orthogonal_to_all_ones(self, dimension, mean=0, std_dev=1):
        random_vector = np.random.normal(mean, std_dev, dimension)
        
        all_ones_vector = np.ones(dimension)
        
        projection = np.dot(random_vector, all_ones_vector) / np.dot(all_ones_vector, all_ones_vector)
        orthogonal_vector = random_vector - projection * all_ones_vector
        
        
        return orthogonal_vector
    
 