import networkx as nx
import csv

class DataReaderNetworkX:
    def __init__(self):
        pass

    def read_csv_simple(self, file_path):
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header if there is one
            data = []
            graph = nx.Graph()
            for row in csv_reader:
                data.append(row)
                graph.add_edge(int(row[0]), int(row[1]), weight=1)

        return graph
        
