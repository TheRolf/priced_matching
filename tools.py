def edge(e):
    e_ = list(e)
    e_[0], e_[1] = e_[1], e_[0]
    e_ = tuple(e_)
    return tuple(e) if e[0] < e[1] else e_
