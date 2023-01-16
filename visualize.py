import pickle
import csv
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
directory='D:\\University\\Bachelor project\\codes\\dataset1'

files=[]
with open(directory+ '\\' + 'your_file2.txt', 'r') as f:
    for item in f:
        files.append(item.strip('\n'))


neighbours=[]
nodes=[]
for net in files:
    if net not in nodes:
        nodes.append(net)
    f = open(directory + '\\' + net + '.edges')
    for count, line in enumerate(f):
        data_line = line.rstrip().split()
        neighbours.append((data_line[0], data_line[1]))

        for item in data_line:
            if (net,item) not in neighbours:
                neighbours.append((net,item))
            if item not in nodes:
                nodes.append(item)


G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(neighbours)
H=G.subgraph(nodes[0:20])

nx.draw(G, with_labels=False)
plt.show()
plt.savefig("graph.pdf")