"""This code is a sample for callgraphs"""

from maraudersmap.sample4callgraph.objs import myObject, external_fun

def fun_foo(aaa:str, bbb:int, ccc:bool=True):
    """Basic function calling a function"""
    fun_void()
    pass
    pass
    pass
    pass
    pass
    pass

def fun_ext():
    """Basic function calling a function of another module"""
    external_fun(43)
    pass

def fun_void():
    """Simplest function"""
    return "dummy"

def fun_bar(aaa, bbb):
    """Calls a function withing a function call"""
    fun_foo(fun_void(),42)
    pass

def main():
    """Instantiate an object"""
    aaa = myObject()
    print(aaa.meth1(42))

def fun_with_obj(aaa:myObject):
    """Use an object in args"""
    aaa.meth1(42)
