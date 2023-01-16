import pickle
import csv
import os
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from functools import partial

directory='D:\\University\\Bachelor project\\codes\\dataset'
directory_pickels='D:\\University\\Bachelor project\\pickels2'

class Node(object):
    def __init__(self, id, follower, following, network, features, feature_names):
        self.id = id
        self.follower = follower             #[id]  id-->node
        self.following = following           #[id]  node-->id
        self.network = network               #[net_id]
        self.features = features             #{network:[feat]}
        self.feature_names = feature_names   #{network:[feat_names]}

def calc_invests(feat_name1, feat_name2,alpha1,alpha2):
    hashtag=0
    mention=0
    for x in feat_name1:
        if x in feat_name2:
            if x[0]=='#':
                hashtag +=1
            else:
                mention += 1
    inv=alpha1*hashtag + alpha2*mention
    inv=inv/40 #changeeeeeeeee
    return inv


def sum_invests(G,B):
    sum_inv=0
    feat_namesB = []
    for name in B.feature_names.values():
        for item in name:
            feat_namesB.append(item)
    for A in B.follower:
        if G.nodes[A]['data'].id==B.id:
            continue
        feat_namesA=[]
        for name in G.nodes[A]['data'].feature_names.values():
            for item in name:
                feat_namesA.append(item)
        sum_inv += math.exp(calc_invests(feat_namesA, feat_namesB, alpha1=1, alpha2=1))
    return sum_inv


def invests(A,B):
    feat_namesB = []
    for name in B.feature_names.values():
        for item in name:
            feat_namesB.append(item)
    feat_namesA = []
    for name in A.feature_names.values():
        for item in name:
            feat_namesA.append(item)
    return math.exp(calc_invests(feat_namesA, feat_namesB,alpha1=1,alpha2=1))


def influence(featnamesA,featnamesB, invB):  #A-->B   #invests(B,A)/sum(invests(B,X))
    invests_AB=math.exp(calc_invests(featnamesA, featnamesB,alpha1=1,alpha2=1))
    if invB==0:
        return 0
    return invests_AB/(invB)

def parallel_inf(feat_names,inv_per_node,edge):
    return influence(feat_names[edge[0]], feat_names[edge[1]], inv_per_node[edge[1]])

def calc_weights(G):
    inv_per_node={}
    feat_names={}
    for num,n in enumerate(G.nodes()):
        inv_per_node[n]=(sum_invests(G,G.nodes[n]['data']))
        feat_names[n] = []
        for name in G.nodes[n]['data'].feature_names.values():
            for item in name:
                feat_names[n].append(item)
    for ind,edge in enumerate(list(G.edges())):
        G[edge[0]][edge[1]]['weight']=influence(feat_names[edge[0]], feat_names[edge[1]], inv_per_node[edge[1]])


def read_neighbour_node(line,net,neighbours,nodes):
    data_line = line.rstrip().split()
    neighbours.add((data_line[0], data_line[1]))
    for item in data_line:
        neighbours.add((net, item))
        nodes.add(item)

def read_data(directory,nodes,neighbours):
    files=[]
    with open(directory+ '\\' + 'your_file.txt', 'r') as f:
        for item in f:
            files.append(item.strip('\n'))
    for net in files:
        nodes.add(net)
        address="%s\\edges\\%s.edges" % (directory, net)
        f = open(address)
        for line in f:
            read_neighbour_node(line, net, neighbours, nodes)


def make_graph(directory_pickels,nodes,neighbours):
    G = nx.DiGraph()
    for item in nodes:
        address="%s\\%s.pkl" %(directory_pickels, item)
        with open(address, 'rb') as f:
            node_obj = pickle.load(f)
        G.add_node(item, data=node_obj)
    G.add_edges_from(neighbours)
    calc_weights(G)
    nx.write_gpickle(G, "graph.gpickle")

nodes=[]
with open('nodes.pkl', 'rb') as f:
    nodes = pickle.load(f)
neighbours=[]
with open('neighbours.pkl', 'rb') as f:
    neighbours = pickle.load(f)

#make_graph(directory_pickels, nodes, neighbours)

G = nx.read_gpickle("graph.gpickle")

import random
#H = G.subgraph(random.sample(nodes,300))
#graphs = list(nx.connected_component_subgraphs(G))
for Gc in sorted(nx.strongly_connected_component_subgraphs(G),key=len, reverse=True):
    if len(Gc)==73:
        H=Gc
        nx.write_gpickle(H, "sub_graph.gpickle")
        break

#H= min(nx.strongly_connected_component_subgraphs(G), key=len)
#nx.draw(H, with_labels=True)
pos = nx.spring_layout(H)
nx.draw(H,pos)
labels=dict([((u,v,),d['weight'])
             for u,v,d in H.edges(data=True)])
#labels = nx.get_edge_attributes(H,'weight')
nx.draw_networkx_edge_labels(H,pos,edgelist=H.in_edges(),edge_labels=labels)
plt.show()


