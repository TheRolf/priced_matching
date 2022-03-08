from fractions import Fraction
from pprint import pprint

import gurobipy
from matplotlib import pyplot as plt
import easygui
from prm_lp import min_maximal_matching, maximum_matching

EPS = 0.15
eps = 0.1
X, Y = 6, 5
env = gurobipy.Env(empty=True)
env.setParam('LogToConsole', 0)
env.start()


def newIndex(vertices):
    i = 0
    while i in vertices.keys():
        i += 1
    return i


def keypress(event):
    global vertices, edge, edges, e_sel, i_sel, x_sel, y_sel, env
    if event.key == 'backspace':
        print("\nRESET\n")
        vertices, edges = {}, []
        reDraw()

    if event.key == 'delete':
        if e_sel:
            print(f"del: {e_sel}")
            edges = [e for e in edges if e != e_sel]
            print(edges)
            e_sel, i_sel = None, None
            edge = []
            reDraw()

        elif i_sel is not None:
            print(f"del: {i_sel}")
            del vertices[i_sel]
            edges = [e for e in edges if i_sel not in e]
            print(edges)
            i_sel = None
            edge = []
            reDraw()

    if event.key == 'x':
        x = min_maximal_matching(edges, weight=weight, env=env)
        y = maximum_matching(edges, weight=weight, env=env)
        reDraw(x)
        plt.text(0.5, 0.5, f"min-max matching: {len(x)} ({Fraction(len(x), len(y))} = {round(len(x)/len(y), 3)})", fontsize=12)

    if event.key == 'y':
        x = maximum_matching(edges, weight=weight, env=env)
        reDraw(x)
        plt.text(0.5, 0.5, f"maximal matching: {len(x)}", fontsize=12)

    if event.key == 'z':
        print(len(vertices), len(edges))
        print(f"vertices = {vertices}")
        print(f"edges = {edges}")

    if event.key == 'w' and i_sel is not None:
        text = easygui.enterbox("", f"Set weight for node {i_sel}")
        w = 0.5 if text == '' else float(text)
        weight[i_sel] = w
        print(f"weight[{i_sel}] := {w}")
        i_sel = None
        edge = []
        reDraw()

    if event.key == 'w' and e_sel is not None:
        pass
        # w = 0.5 if text == '' else float(text)
        # weight[i_sel] = w
        # print(f"weight[{i_sel}] := {w}")
        # i_sel = None
        # edge = []
        # reDraw()

    if event.key == 'd':
        print()
        print(f"i_old = {i_sel}")
        print(f"x_old = {x_sel}")
        print(f"y_old = {y_sel}")
        print(f"e_sel = {e_sel}")
        print(f"edge = {edge}")

    if event.key == 'escape':
        i_sel = None
        e_sel = None
        edge = []
        reDraw()


def onLine(x, y, x1, y1, x2, y2):
    if (abs(x - x1) < EPS and abs(y - y1) < EPS) or (abs(x - x2) < EPS and abs(y - y2) < EPS):
        return False

    crossproduct = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > eps:
        return False

    dotproduct = (x - x1) * (x2 - x1) + (y - y1)*(y2 - y1)
    if dotproduct < 0:
        return False

    squaredlengthba = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    if dotproduct > squaredlengthba:
        return False

    return True


def selectLine(x, y):
    global vertices, edges
    for i, j in edges:
        x1, y1 = vertices[i]
        x2, y2 = vertices[j]
        if onLine(x, y, x1, y1, x2, y2):
            return [i, j]
    else:
        return


def addPoint(x, y):
    global vertices
    for i in vertices:
        x0, y0 = vertices[i]
        if abs(x-x0) < EPS and abs(y-y0) < EPS:
            return i, x0, y0
    else:
        i = newIndex(vertices)
        print(f"add: {i}")
        vertices[i] = [x, y]
        weight[i] = 0.5
        return i, x, y


def reDraw(x_vec=()):
    global vertices, edges, weight
    ax.cla()
    ax.set_aspect(1)
    plt.xlim([0, X])
    plt.ylim([0, Y])
    for i in vertices:
        x, y = vertices[i]
        ax.scatter(x, y, s=40, c='k', zorder=3)
        ax.annotate(f"{i} [{weight[i]}]" if weight[i] != 0.5 else f"{i}", (x+0.05, y+0.05))

    for e in edges:
        i, j = e
        x1, y1 = vertices[i]
        x2, y2 = vertices[j]
        ax.plot((x1, x2), (y1, y2), 'r' if weight[i]+weight[j] > 1 else 'k', zorder=2, linewidth=4 if (i, j) in x_vec or (j, i) in x_vec else 1.5)
    plt.draw()


def reset():
    global x_sel, y_sel, vertices
    x_sel, y_sel = None, None


def onclick(event):
    global e_sel, i_sel, x_sel, y_sel, edge, edges, vertices
    if event.button==1:
        reDraw()
        x, y = round(event.xdata, 1), round(event.ydata, 1)
        e_sel = selectLine(event.xdata, event.ydata)

        if e_sel:
            x1, y1 = vertices[e_sel[0]]
            x2, y2 = vertices[e_sel[1]]
            ax.plot((x1, x2), (y1, y2), 'k', zorder=2, linewidth=4)
            ax.plot((x1, x2), (y1, y2), 'w', zorder=2, linewidth=1.5)

        else:
            i, x, y = addPoint(x, y)
            if i_sel is not None:
                ax.scatter(x, y, s=40, c='k', zorder=3)
                if i != i_sel:
                    ax.scatter(x_sel, y_sel, s=40, c='k', zorder=3)
                    edge.append(i)
                    if edge not in edges and list(reversed(edge)) not in edges:
                        print(f"add: {edge}")
                        edges.append(edge)
                        reDraw()
                edge = []
                i_sel, x_sel, y_sel = None, None, None
            else:
                ax.scatter(x, y, s=40, c='k', zorder=2)
                ax.scatter(x, y, s=25, c='w', zorder=3)
                edge.append(i)
                i_sel, x_sel, y_sel = i, x, y

    if event.button==3:
        if x_sel is not None and y_sel is not None:
            reset()
            reDraw()
    plt.draw()


def submit(b):
    text = b.get(1.0, "end-1c")
    print(text)


vertices = {}
edges = []

# n=8, m=21 1/2-example
# vertices = {0: [1.9, 3.8], 1: [3.4, 3.8], 2: [0.9, 3.0], 3: [0.9, 1.9], 4: [1.9, 1.1], 5: [3.3, 1.1], 6: [4.1, 1.8], 7: [4.1, 3.1]}
# edges = [[0, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [3, 7], [2, 6], [5, 3], [2, 5], [6, 3], [2, 1], [1, 6], [4, 1], [3, 1], [0, 6], [0, 4], [6, 4], [4, 7], [4, 2], [2, 7]]

# grid? with 0.636
# vertices = {0: [2.4, 4.1], 1: [3.1, 4.1], 2: [3.1, 3.4], 3: [2.4, 3.4], 4: [3.2, 2.6], 5: [4.0, 2.6], 6: [4.0, 3.3], 9: [1.6, 3.3], 12: [4.0, 2.0], 13: [4.9, 2.0], 14: [4.8, 2.6], 15: [1.7, 4.1], 16: [4.0, 4.1], 17: [4.8, 4.1], 18: [4.8, 3.3], 19: [3.3, 2.0], 20: [3.3, 1.2], 21: [4.1, 1.1], 22: [2.4, 2.0], 23: [2.4, 1.3], 24: [0.9, 3.3], 25: [1.0, 4.0]}
# edges = [[0, 1], [1, 2], [2, 3], [3, 0], [2, 4], [4, 5], [5, 6], [6, 2], [9, 3], [5, 12], [12, 13], [13, 14], [14, 5], [9, 15], [15, 0], [6, 16], [16, 17], [17, 18], [18, 6], [12, 19], [19, 20], [20, 21], [21, 12], [19, 22], [22, 23], [23, 20], [9, 24], [24, 25], [25, 15]]

edge = []
weight = {}
i_sel, x_sel, y_sel = None, None, None
e_sel = None

fig, ax = plt.subplots(figsize=(12, 9))
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', keypress)
reDraw()

plt.show()
