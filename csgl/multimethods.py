#! /usr/bin/env python
""" Multiple method utility decorator

    C++ Users:  This is the simplest way of mimicing
    operator overloading. 

    Note: As written this decorator only supports
    positional arguments. 
"""

# http://www.artima.com/weblogs/viewpost.jsp?thread=101605
registry = {}

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}

    # self = a MultiMethod instance, instance = the object we want to bind to
    def __call__(self, instance, *args):
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        print("types:",types)
        if function is None:
            raise TypeError("no match")
        return function(instance, *args)

    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function


def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        def getter(instance, *args, **kwargs):
            return mm(instance, *args, **kwargs)
        #return mm
        return getter
    return register

def multimethod2(*types):
    class _multimethod2(object):

        def __init__(self,method):
            self.method = method
            print("Init method:",method)
        def __get__(self,instance,cls):
            print("Getting instance ",instance," of class ",cls)
            return lambda *args, **kw: self.method(cls, *args, **kw)
    
    # can we somehow register the class above here in the registry
    # and then return only 1 instance or create a global class variable 
    # that is assigned information about the original caller?
    #
    print("new multimethod2")
    return _multimethod2

def multiple_decorators(func):
   return classmethod(func)
#@my_dec
#def foo():pass =>  foo = my_ec(f) 
# Python 3.x (needs support for function annotations)
# class MultiMethod(object):
#     def __init__(self, name):
#         self.name = name
#         self.typemap = {}

#     # self = a MultiMethod instance, instance = the object we want to bind to
#     def __call__(self, instance, *args):
#         types = tuple(arg.__class__ for arg in args) # a generator expression!
#         function = self.typemap.get(types)

#         if function is None:
#             raise TypeError("no match")
#         return function(instance, *args)

#     def register(self, types, function):
#         if types in self.typemap:
#             raise TypeError("duplicate registration")
#         self.typemap[types] = function

# def multimethod(function):
#     name = function.__name__
#     mm = registry.get(name)
#     if mm is None:
#         mm = registry[name] = MultiMethod(name)

#     types = tuple(function.__annotations__.values())
#     mm.register(types, function)
#     # return a function instead of a object - Python binds this automatically
#     def getter(instance, *args, **kwargs):
#         return mm(instance, *args, **kwargs)
#     return getter


def main():
    class Foo(object):
        @multimethod()
        def add(self):
            print("Add foo",self)

        @multimethod(int)
        def add(self,value):
            print("Add foo int")

    class Bar(object):
        @multimethod()
        def add(self):
            print("Add bar")
        @multimethod(int)
        def add(self):
            print("Add bar int")

    f = Foo()
    b = Bar()

    f.add(1)
    b.add()

if __name__=="__main__":
    main()
