# Priced Matching


### 1) generate_counterExamples.py

I tried to generate counterexamples for the following strategy: "pick an arbitrary perfect matching M, guarantee that the prices on the matching edges sum up to 1". 

I first generated random graphs using some standard function by networkx. I think it is supposed to generate Erdos-Renyi graphs. I chose n=10 and p somewhere between 0.3 and 0.6. I observed that 0.5 generates counter examples. 

Then, I computed some maximum matching M. If this is not perfect, I set prices on uncovered nodes to be 1. 

Then, I pick for each matching edge in M some arbitrary representative node.

Then, I iterate over all subsets of the representative nodes. If a representative node is in the subset, this is interpreted as being the 'heavy' node of this edge, otherwise it is the light node and its partner becomes the heavy node. 

Then, for the given subset I iterate over all weak orders over the set of representative nodes.

I distinguish two case: case 1) the lowest class gets value 1/2 case 2) the lowest class gets value 1/2 + epsilon. Then, all nodes get their prices according to their class and whether they are heavy or light. (that is, always of the form 1/2 (+/-) z * epsilon, where z is the class). 

Lastly, check whether these prices suffices to guarantee a minmax matching of size 4.

If the example survives the nested for loops, it is deemed a counter example. 


### 2) arguments_counterExamples.py
### 3) test_algorithm_ideas.py




