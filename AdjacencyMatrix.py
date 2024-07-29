import numpy as np  

class AdjacencyMatrix:
    def __init__(self):
        self.adjacency_matrix = {}
        self.vertices = []
        self.num_vertices = 0
        self.num_edges = 0

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.adjacency_matrix[vertex] = {}
            for v in self.vertices:
                self.adjacency_matrix[vertex][v] = 0
                self.adjacency_matrix[v][vertex] = 0
            self.num_vertices+=1

    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.vertices:
            self.add_vertex(vertex1)
        if vertex2 not in self.vertices:
            self.add_vertex(vertex2)

        if vertex1 == vertex2:
            self.adjacency_matrix[vertex1][vertex2] += 1
        else:
            self.adjacency_matrix[vertex1][vertex2] += 1
            self.adjacency_matrix[vertex2][vertex1] += 1
        self.num_edges+=1

    def add_vertices(self, vertices):
        for vertex in vertices:
            self.add_vertex(vertex)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1])

    def get_adjacency_matrix(self):
        num_vertices = len(self.vertices)
        adjacency_np = np.zeros((num_vertices, num_vertices), dtype=int)
        
        for i in range(num_vertices):
            for j in range(num_vertices):
                adjacency_np[i][j] = self.adjacency_matrix[self.vertices[i]][self.vertices[j]]
    
        
        return adjacency_np

    def display(self):
        for vertex in self.vertices:
            print(vertex, ":", [self.adjacency_matrix[vertex][v] for v in self.vertices])


    def get_degree(self, vertex):
        degree_sum = 0
        for i in self.vertices:
            if self.adjacency_matrix[vertex][i] > 0:
                degree_sum+=1
        return degree_sum
    
    def get_degree_vector(self):
        vec = [0]*self.num_vertices
        k = 0
        for i in self.vertices:
            vec[k] = self.get_degree(i)
            k = k+1
        return vec

if __name__ == "__main__":
    graph = AdjacencyMatrix()
    graph.add_vertices([1, 2, 3, 4])
    graph.add_edges([(1, 2), (2, 3), (3, 4), (4, 1), (1, 1)])
    
    
