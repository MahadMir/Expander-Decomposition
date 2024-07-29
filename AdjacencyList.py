import math
import copy

class AdjacencyList:
    def __init__(self, graph_type):
        self.adjacency_list = {}
        self.num_edges = 0
        self.num_vertices = 0
        self.vertices = []
        self.capacity = {}  
        self.graph_type = graph_type
        self.sink_vert = -1
        self.source_vert = -1
        self.make_subdivision_verts = []
        self.make_anti_parallel_edges_verts = []
        self.contains_self_loops = False

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.num_vertices += 1
            self.vertices.append(vertex)

    def get_min_degree(self, vertex):
        curr_min = math.inf
        for vertex in self.graph.adjacency_list:
            curr_min = min(curr_min, self.graph.adjacency_list[vertex])
        return curr_min

    def add_edge(self, vertex1, vertex2, capacity):
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)

        if vertex1 == vertex2:
            self.contains_self_loops = True
            self.adjacency_list[vertex1].append(vertex2)
            self.capacity[(vertex1, vertex1)] = capacity
            if self.graph_type =="simple":
                self.num_edges+=2
            else:
                self.num_edges+=1
        else:
            if self.graph_type=="simple":
                self.adjacency_list[vertex1].append(vertex2)
                self.adjacency_list[vertex2].append(vertex1)
                self.capacity[(vertex1, vertex2)] = capacity
                self.capacity[(vertex2, vertex1)] = capacity 
                self.num_edges += 2
            else:
                self.adjacency_list[vertex1].append(vertex2)
                self.capacity[(vertex1, vertex2)] = capacity
                if (vertex2, vertex1) not in self.capacity:
                    self.capacity[(vertex2, vertex1)] = 0
                self.num_edges +=1


    def remove_antiparallel_edges(self):

        processed_edges = set()
        graph_with_no_antiparallel_edges = AdjacencyList("directed")

        curr_vert_num = self.num_vertices

        for x in self.vertices:
            for y in self.adjacency_list[x]:
                edge = (x, y)
                if x in self.adjacency_list[y]:
                    if edge not in processed_edges:

                        new_vert = curr_vert_num
                        graph_with_no_antiparallel_edges.add_vertex(new_vert)
                        graph_with_no_antiparallel_edges.make_anti_parallel_edges_verts.append(new_vert)
                            

                        graph_with_no_antiparallel_edges.add_edge(x, new_vert, self.capacity.get((x,y), 0))
                        graph_with_no_antiparallel_edges.add_edge(new_vert, y, self.capacity.get((x,y), 0))


                        curr_vert_num+=1

                        new_vert = curr_vert_num
                        graph_with_no_antiparallel_edges.add_vertex(new_vert)
                        graph_with_no_antiparallel_edges.make_anti_parallel_edges_verts.append(new_vert)
                                
                        curr_vert_num+=1

                        graph_with_no_antiparallel_edges.add_edge(y, new_vert, self.capacity.get((y,x), 0))
                        graph_with_no_antiparallel_edges.add_edge(new_vert, x, self.capacity.get((y,x), 0))

                        graph_with_no_antiparallel_edges.set_capacity(x, y, 0)
                        graph_with_no_antiparallel_edges.set_capacity(y, x, 0)

                        processed_edges.add((y, x))
                        processed_edges.add((x, y))
                else:
                    graph_with_no_antiparallel_edges.add_edge(x, y, self.get_capacity(x,y))
                    processed_edges.add((x,y))

        
        return graph_with_no_antiparallel_edges
        

    def make_subdivision_graph(self):

        processed_edges = set()

        subdivision_graph = AdjacencyList(self.graph_type)

        curr_new_vert_number = self.num_vertices

        for x in self.vertices:
                for y in self.adjacency_list[x]:
                    if (x,y) not in processed_edges:
                        if x == y:
                            new_vert = curr_new_vert_number
                            subdivision_graph.add_vertex(new_vert)
                            subdivision_graph.make_subdivision_verts.append(new_vert)
                            subdivision_graph.add_edge(x, new_vert, self.capacity.get((x, y), 0))
                            processed_edges.add((x, y))

                        else:
                            new_vert = curr_new_vert_number
                            subdivision_graph.add_vertex(new_vert)
                            subdivision_graph.make_subdivision_verts.append(new_vert)
                            subdivision_graph.add_edge(x, new_vert, self.capacity.get((x, y), 0))

                            subdivision_graph.add_edge(y, new_vert, self.capacity.get((y,x), 0))

                            if self.graph_type=="simple":
                                processed_edges.add((x, y))
                                processed_edges.add((y, x))
                        
                            else:
                                processed_edges.add((x,y))
                        curr_new_vert_number+=1

        return subdivision_graph


    def remove_anti_parallel_edges_helper(self):
        g = self.remove_antiparallel_edges()
        if self.contains_self_loops:
            return g.remove_anti_parallel_edges()
        else:
            return g

    def get_num_edges(self):
        if self.graph_type =="simple":
            return self.num_edges/2
        else:
            return self.num_edges

    def display(self):
        for vertex in self.adjacency_list:
            edges = []
            for neighbor in self.adjacency_list[vertex]:
                edges.append(f"{neighbor} (capacity: {self.capacity[(vertex, neighbor)]})")
            print(f"{vertex}: {', '.join(edges)}")
        return self


    def display_capacities(self):
        print(self.capacity)

    def induced_subgraph(self, vertices):
        processed_edges = set()
        subgraph_adj_list = AdjacencyList(self.graph_type)
        for vertex in vertices:
            subgraph_adj_list.add_vertex(vertex)
            for neighbor in self.adjacency_list[vertex]:
                if self.graph_type == "simple":
                    if (vertex, neighbor) not in processed_edges:
                        if neighbor in vertices:
                            subgraph_adj_list.add_edge(vertex, neighbor, self.capacity[(vertex, neighbor)])
                            processed_edges.add((vertex,neighbor))
                            processed_edges.add((neighbor,vertex))
                else:
                    if neighbor in vertices:
                        subgraph_adj_list.add_edge(vertex, neighbor, self.capacity[(vertex, neighbor)])
        return subgraph_adj_list
    


    def degree_preserving_induced_subgraph(self, vertices):
        processed_edges = set()
        subgraph_adj_list = AdjacencyList(self.graph_type)
        subgraph_adj_list.num_vertices = 0
        for vertex in vertices:
            subgraph_adj_list.add_vertex(vertex)
            for neighbor in self.adjacency_list[vertex]:
                if self.graph_type == "simple":
                    if (vertex, neighbor) not in processed_edges:
                        if neighbor in vertices:
                            subgraph_adj_list.add_edge(vertex, neighbor, self.capacity[(vertex, neighbor)])
                            processed_edges.add((vertex,neighbor))
                            processed_edges.add((neighbor,vertex))
                        else:
                            subgraph_adj_list.add_edge(vertex, vertex, self.capacity[(vertex, neighbor)])
                else:
                    if neighbor in vertices:
                        subgraph_adj_list.add_edge(vertex, neighbor, self.capacity[(vertex, neighbor)])
                    else:
                        subgraph_adj_list.add_edge(vertex, vertex, self.capacity[(vertex, neighbor)])
        return subgraph_adj_list



    def get_vertex_adjacency_list(self, vertex):
        if vertex in self.adjacency_list:
            return self.adjacency_list[vertex]
        else:
            raise IndexError(f"No Vertex with Index {vertex} Exists")

    def count_num_edges_from_to(self, x, y):
        count = 0
        for z in self.adjacency_list[x]:
            if z == y:
                count+=1

    def get_degree(self, vertex):
        if vertex in self.adjacency_list:
            if self.graph_type=="simple":
                return len(self.adjacency_list[vertex])
            else:
                out_deg = len(self.adjacency_list[vertex])
                in_deg = 0
                for in_vert in self.adjacency_list:
                    if vertex != in_vert:
                        in_deg+=self.count_num_edges_from_to(in_vert, vertex)
                return (out_deg + in_deg)
                        

    def get_degree_vector(self):
        degree_vec = [0] * self.num_vertices
        i = 0
        for v in self.adjacency_list:
            degree_vec[i] = self.get_degree(v)
            i += 1
        return degree_vec
    
    def get_degree_vector_dict(self):
        degree_vec = {}
        i = 0
        for v in self.adjacency_list:
            degree_vec[i] = self.get_degree(v)
            i += 1
        return degree_vec

    def get_capacity(self, u, v):
        return self.capacity.get((u, v), 0)

    def set_capacity(self, u, v, capacity):
        self.capacity[(u, v)] = capacity


    def get_min_degree(self):
        degrees = self.get_degree_vector()
        min_deg = math.inf
        for deg in degrees:
            min_deg = min(deg, min_deg)
        return min_deg    

    def make_edge_from_super_source_to_vert(self, vert):
        self.source_vert = self.num_vertices
        self.add_vertex(self.source_vert)
        self.add_edge(self.source_vert, vert, math.inf)
        return self

    def make_edge_from_super_source_to_vertices(self, verts):
        for vert in verts:
            self.make_edge_from_super_source_to_vert(vert)
        return self

    def make_edge_from_vert_to_super_sink(self, vert):
        self.sink_vert = self.num_vertices
        self.add_vertex(self.sink_vert)
        self.add_edge(vert, self.sink_vert, math.inf)
        return self

    def make_edge_from_verts_to_super_sink(self, verts):
        for vert in verts:
            self.make_edge_from_vert_to_super_sink(vert)

        return self


    def get_volume(self):
        deg = self.get_degree_vector()
        return sum(deg)
    
    def get_volume_vertices(self, vertices):
        sum = 0
        for vertex in vertices:
            sum+=self.get_degree(vertex)
        return sum

    def has_zero_degree_verts(self):
        for vertex in self.vertices:
            if self.get_degree(vertex) == 0:
                return True
        return False
    
    def get_zero_degree_verts(self):
        zero_deg = []
        for vertex in self.vertices:
            if self.get_degree(vertex) == 0:
                zero_deg.append(vertex)
        return zero_deg

    def remove_vertices(self, verts):
        for vertex in verts:
            self.adjacency_list.pop(vertex)
            self.vertices.remove(vertex)

    def only_loops_to_itself(self, vertex):
        only_goes_to_itself = True
        for neighbour in self.adjacency_list[vertex]:
            if neighbour != vertex:
                only_goes_to_itself = False
        return only_goes_to_itself


    def get_and_remove_subdivision_graph_vertices_which_loop(self):

        vertex_list = copy.deepcopy(self.vertices)
        removed_vertices = []
        for vertex in vertex_list:
            if self.only_loops_to_itself(vertex):
                self.adjacency_list.pop(vertex)
                self.vertices.remove(vertex)
                removed_vertices.append(vertex)
        
        self.make_subdivision_verts = list(set(self.make_subdivision_verts).intersection(set(self.vertices)))
        return removed_vertices