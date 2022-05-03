import random

import gurobipy
import networkx as nx

from prm_lp import maximum_matching, min_maximal_matching

from tqdm import tqdm
from datetime import datetime
from itertools import chain, combinations

def weakorders(A):
    if not A:  # i.e., A is empty
        yield []
        return
    for k in range(1, len(A) + 1):
        for B in combinations(A, k):  # i.e., all nonempty subsets B
            for order in weakorders(set(A) - set(B)):
                yield [B] + order

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    

for _ in range(10000):
    #generate graph randomly (standard erdos graph)
    G = nx.fast_gnp_random_graph(10,0.5)
    
    #fix arbitrary matching to be the perfect matching
    M = list(maximum_matching(G.edges().keys()))
    Mp = list(min_maximal_matching(G.edges().keys()))
    
    if (len(Mp) >= 2/3*len(M)):
        print('trivial prices work')
        continue
    

    covered_M = [i for (i,j) in M] + [j for (i,j) in M]

    p = dict.fromkeys(G.nodes(), 1/2)

    for v in set(G.nodes()) - set(covered_M):
        p[v] = 1


    M_rep = [e[0] for e in M]
    M_dual = {e[0]:e[1] for e in M}

    feasible_edges = [e for e in G.edges() if p[e[0]] + p[e[1]] <= 1]

    found = False
    #iterate over all possible subsets of the representative nodes (if v is in plus, then it will be a heavy node)
    for plus in tqdm(powerset(M_rep)):
        for order in tqdm(weakorders(M_rep)):
            for i in range(2):
                z = len(order) + i - 1
                for oclass in order:
                    for v in oclass:
                        if v in plus:
                            p[v] = 1/2 + epsilon*z
                            p[M_dual[v]] = 1/2 - epsilon*z
                        else:
                            p[v] = 1/2 - epsilon*z
                            p[M_dual[v]] = 1/2 + epsilon*z
                    z = z - 1
                Mp = min_maximal_matching([e for e in G.edges() if p[e[0]] + p[e[1]] <= 1])
                #print(Mp)
                if (len(Mp)>= 2/3*len(M)):
                    print('we found prices')
                    print(p)
                    found = True
                    break
                else:
                    continue
            else:
                continue
        else:
            continue
        break

    if (found == False):
        print('no prices, this is a counter example')
        print(G)
        nowt = datetime.now().strftime('%H%H%m%m%s%s')
        nx.write_edgelist(G, "counterExamples/counterExample"+ nowt + ".edgelist.gz")
