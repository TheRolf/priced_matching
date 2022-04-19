import gurobipy
from gurobipy.gurobipy import GRB


def maximum_matching(edges, weight=None, env=None):
	nodes = sorted([v for e in edges for v in e])
	weight = weight if weight else {v: 0.5 for v in nodes}
	edges = [tuple(sorted(edge)) for edge in sorted(edges)] # if weight[edge[0]] + weight[edge[1]] <= 1]

	if env is None:
		env = gurobipy.Env(empty=True)
		env.setParam('LogToConsole', 0)
		env.start()

	model = gurobipy.Model("max_m", env=env)
	x = model.addVars(list(edges), vtype=GRB.BINARY, name="x")
	model.setObjective(sum(x[e]*(2-weight[e[0]]-weight[e[1]]) for e in edges), GRB.MAXIMIZE)
	model.addConstrs(sum(x[e] for e in edges if v in e) <= 1 for v in nodes)
	model.optimize()

	res = {}
	for e in edges:
		if x[e].X > 0:
			res[e] = x[e].X
	return res


def min_maximal_matching(edges, weight=None, env=None):
	nodes = sorted([v for e in edges for v in e])
	weight = weight if weight else {v: 0.5 for v in nodes}
	edges = [tuple(sorted(edge)) for edge in sorted(edges) if weight[edge[0]] + weight[edge[1]] <= 1]
	if env is None:
		env = gurobipy.Env(empty=True)
		env.setParam('LogToConsole', 0)
		env.start()

	model = gurobipy.Model("max_m", env=env)
	x = model.addVars(list(edges), vtype=GRB.BINARY, name="x")

	model.setObjective(sum(x[e] for e in edges), GRB.MINIMIZE)
	model.addConstrs(sum(x[f] for f in edges if len(set(e).intersection(f)) > 0) >= 1 for e in edges)
	model.addConstrs(sum(x[e] for e in edges if v in e) <= 1 for v in nodes)
	model.optimize()

	res = {}
	for e in edges:
		if x[e].X > 0:
			res[e] = x[e].X
	return res


def ordered_matching(ordered_edges, env=None):
	nodes = sorted([v for e in ordered_edges for v in e])
	ordered_edges = [tuple(sorted(edge)) for edge in ordered_edges]
	if env is None:
		env = gurobipy.Env(empty=True)
		env.setParam('LogToConsole', 0)
		env.start()

	model = gurobipy.Model("ord_m", env=env)
	x = model.addVars(ordered_edges, vtype=GRB.BINARY, name="x")
	y = model.addVars(ordered_edges, vtype=GRB.BINARY, name="y")
	w = model.addVars(nodes, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="w")

	model.setObjective(sum(x[e] for e in ordered_edges), GRB.MAXIMIZE)
	model.addConstrs(y[e] >= 1 - (w[e[0]] + w[e[1]]) for e in ordered_edges)
	model.addConstrs(x[e] <= 1-y[f]+x[f]  for i, e in enumerate(ordered_edges) for j, f in enumerate(ordered_edges) if j < i)
	model.addConstrs(sum(x[e] for e in ordered_edges if v in e) <= 1 for v in nodes)
	model.optimize()

	res = {}
	for e in ordered_edges:
		if x[e].X > 0:
			res[e] = x[e].X
	return res
