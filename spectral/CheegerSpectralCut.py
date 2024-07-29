import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import laplacian
from scipy.sparse import csgraph
import math
import copy
import time




def find_second_eigenvector(graph):
   
    
    L = nx.normalized_laplacian_matrix(graph)
    
    eigenvalues, eigenvectors = eigsh((L), k=2, which='SM')
    
    x1 = eigenvectors[:,1]

    return x1 


def find_cut_edges_for_vert(graph, left_set, vert):
    sum_edges = 0
    for node in left_set:
        if graph.has_edge(node, vert):
            sum_edges+=1
    return graph.degree(vert)-2*sum_edges 

def spectral_cut(graph):
    second_eigenvector = find_second_eigenvector(graph)
    temp = list(graph.nodes)

    nodes = [(temp[i], second_eigenvector[i]) for i in range(len(temp))]
    sorted_nodes_with_values = sorted(nodes, key=lambda x: x[1])


    s_degree = 0
    r_degree = 2*graph.number_of_edges()
    num_cut = 0

    min_conductance_left_set = []
    min_conductance_right_set = []

    min_conductance = math.inf
    remaining_nodes = len(nodes)

    left_nodes = []
    right_nodes = [i for (i, node) in sorted_nodes_with_values]
    
    for node, _ in sorted_nodes_with_values:
        num_cut+=find_cut_edges_for_vert(graph, left_nodes, node)
        left_nodes.append(node)
        right_nodes.pop(0)
        remaining_nodes-=1
        s_degree += graph.degree[node]
        r_degree -= graph.degree[node]
        min_deg = min(s_degree, r_degree)
        new_conductance = (num_cut/ min_deg) if not (len(left_nodes) == 0 or len(left_nodes) == len(sorted_nodes_with_values)) else 1
        new_smallest_conductance_set = (min_conductance > new_conductance)
        if new_smallest_conductance_set:
            min_conductance_left_set = copy.deepcopy(left_nodes)
            min_conductance_right_set = copy.deepcopy(right_nodes)
            min_conductance = new_conductance

        print((remaining_nodes, min_conductance, new_conductance, len(min_conductance_left_set), len(min_conductance_right_set)))

    return (min_conductance_left_set, min_conductance_right_set, min_conductance)
