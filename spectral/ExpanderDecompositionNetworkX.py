from CheegerSpectralCut import spectral_cut
from ReadDataNetworkX import DataReaderNetworkX
import networkx as nx
import math
from RandomConnectednecteGraph import generate_connected_graph

def recursive_split_expander(g, conductance, total_node_set, original_graph):
    if len(g.nodes()) <= 2:
        for node in g.nodes():
            node_set = set()
            node_set.add(node)
            total_node_set.add(frozenset(node_set))
    else:
        left, right, min_conductance = spectral_cut(g)
        if min_conductance >= conductance:
            node_set = set()
            node_set.add(frozenset(g.nodes()))
            total_node_set.add(frozenset(node_set))
        else:
            left_induced = g.subgraph(left).copy()
            right_induced = g.subgraph(right).copy()
            total_node_set.update(recursive_split_expander(left_induced, conductance, set(), original_graph))
            total_node_set.update(recursive_split_expander(right_induced, conductance, set(), original_graph))
    return total_node_set

def recursive_split_expander_helper(g, conductance):
    return recursive_split_expander(g, conductance, set(), g)

path = "/Users/mahad/Documents/Dissertation/data/deezer_clean_data"
reader = DataReaderNetworkX()
graph = reader.read_csv_simple(path + "/RO_edges.csv")
graph = generate_connected_graph(250, 7)


graph_cluster = recursive_split_expander_helper(graph, 0.9)

for outer_frozenset in graph_cluster:
    print("Outer frozenset:")
    for inner_frozenset in outer_frozenset:
        print("  Inner frozenset elements:", inner_frozenset)
