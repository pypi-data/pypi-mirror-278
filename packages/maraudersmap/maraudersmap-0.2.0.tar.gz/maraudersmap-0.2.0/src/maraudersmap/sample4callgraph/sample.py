"""Sample code to illustrate the usage of dynamic callgraph generation..."""

def fuuun( x, y, opt=False):
    out =  addition(x,y)

    if out >10:
        out = toobig(out)

    if opt:
        maybemaybenot()
    return out

def addition(x,y):
    return y+x

def toobig(x):
    return x-10

def maybemaybenot():
    pass
    return 


