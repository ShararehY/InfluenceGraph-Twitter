import pickle
import time
"""import multiprocessing
from functools import partial
from itertools import repeat
import csv
import os
import numpy as np"""
directory='D:\\University\\Bachelor project\\codes\\dataset'

#run it only the first time
"""nets=[]
for filename in os.listdir(directory):
    if filename.endswith(".edges"):
        net = filename.strip('.edges')
        nets.append(net)
with open('network.txt', 'w') as f:
    for item in nets:
        f.write("%s\n" % item)"""


class Node(object):
    def __init__(self, id, follower, following, network, feature_names):
        self.id = id
        self.follower = follower
        self.following = following
        self.network = network
        #self.features = features
        self.feature_names = feature_names

def create_featnames(line):
    data_line = line.rstrip().split('\t')
    return data_line[0].split()[1]

def read_neighbour_net_node(data_line,net,neighbours, network, nodes):   #find neighbours and network of nodes
    #neighbours.append(data_line)
    for item in data_line:
        neighbours.append(item)
        if item in nodes:
            if net not in network[nodes.index(item)]:
                network[nodes.index(item)].append(net)
        else:
            nodes.append(item)
            network.append([net])


neighbours = []
nodes = []
network = []
list_egos = []

with open('network.txt', 'r') as f:
    for item in f:
        list_egos.append(item.strip('\n'))

n=0
for net in list_egos:
    address = "%s\\edges\\%s.edges" % (directory, net)
    f = open(address)
    neighbours.append([])
    for line in f:
        data_line = line.rstrip().split()
        read_neighbour_net_node(data_line, net, neighbours[n], network, nodes)
    n += 1


for ind,ego in enumerate(list_egos):
    followings = set()
    followers=set()
    featurenames={}
    features={}
    if ego not in nodes:
        for nei in neighbours[ind]:
            followings.add(nei)
        networks_of_id=[ego]
        f = open("%s\\featnames\\%s.featnames" % (directory, ego))
        feat_names = []
        feat_names=list(map(create_featnames, f))
        featurenames[ego] = feat_names

        f = open("%s\\egofeat\\%s.egofeat" % (directory, ego))
        for line in f:
            data_line = line.rstrip().split('\t')
            features[ego] = data_line[0].split()

        one_features = []
        name_one_features=[]
        for ind,feat in enumerate(features[ego]):
            if feat=='1':
                one_features.append(feat)
                name_one_features.append(featurenames[ego][ind])

        features[ego]=one_features
        featurenames[ego]=name_one_features

        with open(ego+'.pkl', 'wb') as output:
            node_inst = Node(ego,followers,followings,networks_of_id,featurenames)
            pickle.dump(node_inst, output)
        del node_inst



for ind,id in enumerate(nodes):
    followers=set()
    followings=set()
    featurenames={}
    features={}
    networks_of_id=network[ind]
    indexes=[]
    for x,net in enumerate(list_egos):
        for y in networks_of_id:
            if net==y:
                indexes.append(x)
    for n in indexes:  # n:number of networks for each node
        for count,nei in enumerate(neighbours[n]):
            if nei==id:
                if(count%2==0):
                    followings.add(neighbours[n][count+1])
                else:
                    followers.add(neighbours[n][count-1])
        f = open("%s\\featnames\\%s.featnames" % (directory, str(list_egos[n])))
        featurenames[list_egos[n]]=list(map(create_featnames, f))

        if id not in list_egos:
            for item in networks_of_id:
                followers.add(item) #
            f = open("%s\\feat\\%s.feat" % (directory, str(list_egos[n])))
            feats=[]
            for count, line in enumerate(f):
                data_line = line.rstrip().split('\t')
                l=data_line[0].split()
                if l[0]==id:
                    feats=l[1:]
                    features[list_egos[n]]=feats
                    break
        else:
            f = open("%s\\egofeat\\%s.egofeat" % (directory, str(list_egos[n])))
            for item in neighbours[n]:
                followings.add(item)
            networks_of_id.append(id)
            for count, line in enumerate(f):
                data_line = line.rstrip().split('\t')
                features[list_egos[n]] = data_line[0].split()

        one_features = []
        name_one_features = []
        for inde, feat in enumerate(features[list_egos[n]]):
            if feat == '1':
                one_features.append(feat)
                name_one_features.append(featurenames[list_egos[n]][inde])

        features[list_egos[n]] = one_features
        featurenames[list_egos[n]] = name_one_features

    with open(id + '.pkl', 'wb') as output:
        node_inst = Node(id, followers, followings, networks_of_id,  featurenames)
        pickle.dump(node_inst, output)
    del node_inst




