# Priced Matching

## Info

### Dependencies:

`gurobi` solver and `gurobipy` & `matplotlib` python packages

### Usage
run `interactive.py` then draw a graph
- add vertices and edges: `left` mouse click
- remove a vertex or an edge: left click to select then `DEL`
- erase the board: `BACKSPACE`
- calculate and plot min-max matching: `x`
- calculate and plot maximal matching: `y`
- print vertices and edges: `z`

## Gurobi

1. [Register](https://www.gurobi.com/) with your university email address

2. Download "Gurobi Optimizer" from [HERE](https://www.gurobi.com/downloads/)

3. Licence
- If you don't have a licence yet: ask for a free academic licence [HERE](https://www.gurobi.com/downloads/end-user-license-agreement-academic/)
- If you already have a licence: check your licences under [THIS](https://www.gurobi.com/downloads/licenses/) page.

4. Find the line with the form `grbgetkey a1b2c3d4-a1b2-c3d4-a1b2-c3d4a1b2c3d4` and copy it to your clipboard

5. Open a **new** command line / terminal, paste and hit enter

_To make it work under Python_

6. Install Python

7. Install the `gurobipy` package via `pip`: `python -m pip install -i https://pypi.gurobi.com gurobipy`. If this wouldn't work, check the [HELP](https://www.gurobi.com/documentation/9.1/quickstart_windows/cs_using_pip_to_install_gr.html)
