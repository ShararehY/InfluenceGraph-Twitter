import numpy as np
import random
import networkx as nx


class Node(object):
    def __init__(self, id, follower, following, network, features, feature_names):
        self.id = id
        self.follower = follower             #[id]  id-->node
        self.following = following           #[id]  node-->id
        self.network = network               #[net_id]
        self.features = features             #{network:[feat]}
        self.feature_names = feature_names   #{network:[feat_names]}

class Social_Agent(object):
    def __init__(self,id,alpha0,beta0,etha,following,weights):
        self.id=id
        self.alpha=np.array(alpha0)
        self.beta=np.array(beta0)
        self.etha=etha
        self.following=following
        #self.follower=follower
        self.weights=weights
        if alpha0==0 and beta0==0:
            self.state=0.5
        else:
            self.state=alpha0/(alpha0+beta0)

    def observe(self,s):
        self.s=np.array(s)

    def parameter_setter(self,etha):
        self.etha=etha

    def parameter_getter(self):
        return self.etha, self.alpha, self.beta

    def update(self,sum_alpha,sum_beta):
        self.alpha = (1 - self.etha)*(self.alpha + self.s)+ self.etha*sum_alpha#communicate(self.id)[0]
        self.beta = (1 - self.etha)*(self.beta + (1-self.s)) + self.etha*sum_beta#communicate(self.id)[1]
        self.state=self.alpha/(self.aplha+ self.beta)

def communicate(id):
    ind=list_id.index(id)
    sum_alpha=0
    sum_beta=0
    for following in list_followings[ind]:
        ind_following=list_id.index((following))
        sum_alpha+=list_alpha[ind_following]*list_weights[ind][ind_following]
        sum_beta+=list_beta[ind_following]
    return sum_alpha,sum_beta


alpha_bound=1
beta_bound=1
etha=0.5  #change
agents=[]
list_alpha=[]
list_beta=[]
list_id=[]
list_followings=[]
list_weights=[]
G=nx.read_gpickle("sub_graph.gpickle")


for id in G.nodes():
    list_id.append(id)

for n,id in enumerate(G.nodes()):
    #list_id.append(id)
    followings=G.nodes[id]['data'].following
    list_followings.append([])
    list_weights.append([])
    for nei in followings:
        if nei in list_id:
            list_followings[n].append(nei)
    alpha=random.uniform(0,alpha_bound)
    list_alpha.append(alpha)
    beta=random.uniform(0,beta_bound)
    list_beta.append(beta)
    for nei in list_followings[n]:
        list_weights[n].append(G[id][nei]['weight'])
    agents.append(Social_Agent(id,alpha,beta,etha,list_followings[n],list_weights[n]))

for id in list_id:
    communicate(id)





