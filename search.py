import random

import gurobipy
import networkx as nx

from prm_lp import maximum_matching, min_maximal_matching


def random_weights(G, p):
    H = nx.Graph()
    weights = {v: 0.5 + 0.001 if random.random() < p else 0.5 - 0.001 for v in G.nodes}
    for u, v in G.edges:
        if weights[u] + weights[v] <= 1:
            H.add_edge(u, v)
    return H, weights


def search(G, env=None):
    OPT = len(maximum_matching(G, env))
    H, w = random_weights(G, random.random())
    # print(H.edges, end=" ")
    ALG = len(min_maximal_matching(H, env))
    return ALG/OPT


def best_strategy(G, N=10000, env=None):
    best_strategy = 0
    for k in range(N):
        ratio = search(G, env)
        if ratio > best_strategy:
            best_strategy = ratio
    return best_strategy


if __name__ == '__main__':
    env = gurobipy.Env(empty=True)
    env.setParam('LogToConsole', 0)
    env.start()
    while True:
        n, p = random.randint(6, 11), random.uniform(0.05, 0.8)
        G = nx.gnp_random_graph(n, p)
        best = best_strategy(G, env=env)
        print(best, n, p, G.edges)
        if best < 0.66:
            break
