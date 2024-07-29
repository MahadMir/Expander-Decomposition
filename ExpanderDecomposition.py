from CutMatching import CutMatching
from Trimming import Trimming

class ExpanderDecomposition:
    def __init__(self):
        pass

    def decomposition(self, G, phi):
        cut_matching = CutMatching(G, phi, 1, 1)
        A, R, i = cut_matching.cut_matching()
        if i == 0:
            return set(G)
        elif i == 1:
            print("Balanced Cut Returned")
            return self.decomposition(G.degree_preserving_induced_subgraph(list(A)), phi) + \
        self.decomposition(G.degree_preserving_induced_subgraph(list(R)), phi)
        else:
            print("Unbalanced Cut Returned")
            A_prime = Trimming(G, A, phi)
            graph_vertices = set(G.vertices)
            remaining_graph_vertices = graph_vertices - A_prime

            return A_prime + self.decomposition(G.degree_preserving_induced_subgraph(list(remaining_graph_vertices)), phi)