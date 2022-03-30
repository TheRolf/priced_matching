import random

import gurobipy

from prm_lp import maximum_matching, min_maximal_matching


#algorithm ideas
#strategy three_paths shifts epsilon only to paths of length 3, otherwise shift epsilon to all nodes on the other side of independent set nodes
#strategy expDecay decreases epsilon exponentially from round to round

strategy=('three_paths','expDecay')

if(strategy[1]=='expDecay'):
    epsilon = 0.2
else:
    epsilon = 0.001

condition = False

while condition:
    Mp = min_maximal_matching([e for e in G.edges() if p[e[0]] + p[e[1]] <= 1])
    
    print(Mp)
    print(len(Mp))
    print(len(M))
    if len(Mp) >= (2/3)*(len(M)):
        condition = False
    
    else:
        uncovered_Mp = list(set(covered_M) - set([i for (i,j) in Mp] + [j for (i,j) in Mp]))
        
        dict1 = {e[0]:e[1] for e in M if e[1] in uncovered_Mp}
        dict2 = {e[1]:e[0] for e in M if e[0] in uncovered_Mp}
        
        dual_dict = {**dict1, **dict2}
        
        dual_uncovered_Mp = dual_dict.keys()
        
        if(strategy[0]=='all_paths'):
            for v in uncovered_Mp:
                p[v] = p[v] - epsilon
            for e in M:
                if e[0] in uncovered_Mp:
                    p[e[1]] = p[e[1]] + epsilon
                if e[1] in uncovered_Mp:
                    p[e[0]] = p[e[0]] + epsilon
        if(strategy[0]=='three_paths'):
            for e in Mp:
                if e[0] in dual_uncovered_Mp and e[1] in dual_uncovered_Mp:
                    p[e[0]] = p[e[0]] + epsilon
                    p[e[1]] = p[e[1]] + epsilon
                    p[dual_dict[e[0]]] = p[dual_dict[e[0]]] - epsilon
                    p[dual_dict[e[1]]] = p[dual_dict[e[1]]] - epsilon
                    
        if(strategy[1]=='expDecay'):
            epsilon = epsilon/8
        
    print(p)
    print(epsilon)

    


        

    









