


import random
import gurobipy
import networkx as nx

from prm_lp import maximum_matching, min_maximal_matching
#from tqdm import tqdm
#from datetime import datetime

#from itertools import chain, combinations, permutations



for i in range(1,8):

    countexample = 'counterExamples/counterExample' + str(i) + '.edgelist'
    G = nx.read_edgelist(countexample)

    M = list(maximum_matching(G.edges.keys()).keys())

    S = list(set(G.edges().keys()) - set(M))


    for e in G.edges():
        print(e)
    print(M)

    #Step 1) try to find all minmax matchings in this graph (that have only two non-max-edges)

    collect = set([])
    for e1 in G.edges.keys():
        remaining1 = [f for f in S if set(e1).intersection(f) == set([])]
        for e2 in remaining1:
            remaining2 = [f for f in remaining1 if set(e2).intersection(f) == set([])]
            for e3 in remaining2:
                #check whether [e1,e2,e3] is a maximal matching
                if(all(set(f).intersection(e2+e3) != set([]) for f in remaining1)):
                    l = sorted([e1[0]+e1[1],e2[0]+e2[1],e3[0]+e3[1]])
                    s = l[0] + '-' + l[1] + '-' + l[2]
                    collect = collect.union([s])
    for c in collect:
        print(c)


    with open('counterExamples/counterExample' + str(i) + '.txt', 'w') as f:
        f.writelines('Maximum matching returned by gurobi: \n')
        f.writelines(str(M))
        f.writelines('\n')
        f.writelines('Minmax matchings: \n')
        for c in collect:
            f.writelines(c + '\n')
