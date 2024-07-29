import networkx as nx
import random
from AdjacencyList import AdjacencyList
import matplotlib.pyplot as plt

def generate_connected_graph(n, p):
    while True:
        G = nx.erdos_renyi_graph(n, p, seed=42)
        if nx.is_connected(G):
            return G

def convert_networkx_graph_to_adj_list(G):
    t = AdjacencyList("simple")
    for node in G.nodes:
        t.add_vertex(node)
    
    for u, v, data in G.edges(data=True):
        capacity = data.get('capacity', 0)  # Default capacity to 0 if not specified
        t.add_edge(u, v, capacity)

    return t

