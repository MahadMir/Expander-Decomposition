from AdjacencyList import AdjacencyList
import csv
import math
import networkx as nx
import matplotlib.pyplot as plt


class DataReader:
    def __init__(self):
        pass

    def read_csv_simple(self, file_path):
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header if there is one
            data = []
            csv_graph = AdjacencyList("simple")
            for row in csv_reader:
                data.append(row)
                csv_graph.add_edge(int(row[0]), int(row[1]), 1)

        return csv_graph
        

    

if __name__ == '__main__':
    path = "/Users/mahad/Documents/Dissertation/data/deezer_clean_data"
    reader = DataReader()
    graph = reader.read_csv_simple(path +  "/RO_edges.csv")
    
