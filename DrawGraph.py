from AdjacencyList import AdjacencyList
import networkx as nx
import matplotlib.pyplot as plt
from PushRelabel import PushRelabel    
import numpy as np
from ReadData import DataReader
import copy
from CutMatching import CutMatching
from RandomConnectedGraph import generate_connected_graph
from RandomConnectedGraph import convert_networkx_graph_to_adj_list
import cProfile
from ExpanderDecomposition import ExpanderDecomposition

def display_simple_graph(adjacency_list):
    G = nx.Graph()
    
    # Add nodes
    for node in adjacency_list:
        G.add_node(node)
    
    # Add edges
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    # Draw the graph
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, font_size=12, font_weight='bold')
    plt.show()

def display_directed_graph(adjacency_list):
    G = nx.DiGraph()
    
    # Add nodes
    for node in adjacency_list:
        G.add_node(node)
    
    # Add edges
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, arrows=True, font_size=12, font_weight='bold')
    
    plt.title('Directed Graph')
    plt.show()

def display_directed_graph_with_capacities(adjacency_list, capacities):
    G = nx.DiGraph()
    
    # Add nodes
    for node in adjacency_list:
        G.add_node(node)
    
    # Add edges with capacities
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if (node, neighbor) in capacities:
                capacity = capacities[(node, neighbor)]
                G.add_edge(node, neighbor, capacity=capacity)
            else:
                # Handle the case where capacities are not specified for all edges
                G.add_edge(node, neighbor)
    
    # Extract edge capacities for labels
    edge_labels = {(node, neighbor): G.edges[(node, neighbor)]['capacity'] if 'capacity' in G.edges[(node, neighbor)] else None
                   for node, neighbors in adjacency_list.items() 
                   for neighbor in neighbors}
    
    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True,
                           arrowstyle='-|>', arrowsize=15, edge_color='b', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    plt.title('Directed Graph with Capacities')
    plt.axis('off')
    plt.show()

def convert_to_networkx(g):
    G = nx.DiGraph()  # Create a directed graph

    for vertex in g.adjacency_list:
        G.add_node(vertex)
        for vert in g.adjacency_list[vertex]:
            G.add_edge(vertex, vert, capacity=g.capacity[(vertex, vert)])

    return G


def convert_to_networkx_multigraph(g):
    G = nx.MultiDiGraph()  # Create a directed graph

    for vertex in g.adjacency_list:
        G.add_node(vertex)
        for vert in g.adjacency_list[vertex]:
            G.add_edge(vertex, vert, capacity=g.capacity[(vertex, vert)])

    return G

def adjaceny_matrix_and_capacity_matrix(G):
    nodes = list(G.nodes)
    n = len(nodes)

    # Create the adjacency matrix
    adj_matrix = np.zeros((n, n), dtype=int)
    for i, j in G.edges():
        adj_matrix[i, j] = 1

    # Create the capacity matrix
    cap_matrix = np.zeros((n, n), dtype=float)
    for i, j, w in G.edges(data='capacity'):
        cap_matrix[i, j] = w

    return (adj_matrix, cap_matrix)


#path = "/Users/mahad/Documents/Dissertation/data/deezer_clean_data"
#reader = DataReader()
#graph = reader.read_csv_simple(path +  "/RO_edges.csv")


networkx_random_graph = generate_connected_graph(250, 7)
graph = convert_networkx_graph_to_adj_list(networkx_random_graph)


#cut_match = CutMatching(graph, 0.6, 1, 1)
#cut_match.cut_matching()

x = ExpanderDecomposition()
x.decomposition(graph, 0.6)


