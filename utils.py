import math
from typing import Any

class stdinp:
    def __init__(self, symbol):
        self.symbol = symbol
        self.val = None
    
    def __str__(self) -> str:
        return self.symbol
    
    def setval(self, val):
        self.val = val
    
    def __call__(self, args):
        self.setval(args[0])
        return args[0]
    
    def __add__(self, other):
        if self.val is not None:
            return self.val + other
        else:
            return Add([self, other])
    
    def __mul__(self, other):
        if self.val is not None:
            return self.val * other
        else:
            return Mul([self, other])
    
    def __neg__(self):
        if self.val is not None:
            return -self.val
        
        else:
            return Mul([-1, self])
    
    def __sub__(self, other):
        return self + (-other)
    __rmul__ = __mul__
    __radd__ = __add__

    def diff(self):
        x = stdinp("x")
        x.val = 1
        return x


class Add:
    def __init__(self, array) -> None:
        self.array = array[:]
        self.smpl = self.array[:]
        q = True
        for i in range(len(self.array)):
            for j in range(len(self.array)):
                if i != j and type(self.array[i]) is type(self.array[j]):
                    q = False
                    break
            if not q:
                break
        if not q:
            self.smpl = self.simplify().array[:]
        
        self.array = self.smpl[:]
    
    def simplify(self):
        type_dict = {}
        for i in self.array:
            if type(i) in type_dict.keys():
                type_dict[type(i)].append(i)
            else:
                type_dict.update({type(i) : [i]})
        type_arr = type_dict.items()[:]
        res_arr = []
        for t, i in type_arr:
            res_arr.append(sum(i))
        
        return Add(res_arr[:])
    
    def __str__(self) -> str:
        x = self.simplify()
        return "+".join([str(i) for i in x.array])
    
    def __call__(self, args): # args = [(type I, inp I), (type II, inp II), ...]
        z = dict(args[:])
        return sum([i(z(type(i))) for i in self.array])
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Add(self.array[:] + [other])
        return Add(self.array[:] + other.array[:])
    
    def __neg__(self,):
        return Add([-i for i in self.array])
    
    def __sub__(self, other):
        return self + (-other)
    
    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass
    __rmul__ = __mul__
    __radd__ = __add__

    def diff(self):
        return Add([i.diff() if hasattr(i, 'diff') else 0 for i in self.smpl])

class Mul:
    def __init__(self, array) -> None:
        self.array = array[:]
        self.smpl = self.array[:]
        q = True
        for i in range(len(self.array)):
            for j in range(len(self.array)):
                if i != j and type(self.array[i]) is type(self.array[j]):
                    q = False
                    break
            if not q:
                break
        if not q:
            self.smpl = self.simplify().array[:]
        
        self.array = self.smpl[:]
    
    def simplify(self):
        type_dict = {}
        for i in self.array:
            if type(i) in type_dict.keys():
                type_dict[type(i)].append(i)
            else:
                type_dict.update({type(i) : [i]})
        type_arr = type_dict.items()[:]
        res_arr = []
        for t, i in type_arr:
            j = Mul([])
            for k in i:
                j *= k
            res_arr.append(j)
        
        return Mul(res_arr[:])
    
    def __str__(self) -> str:
        x = self.simplify()
        return "*".join([str(i) for i in x.array])
    
    def __call__(self, args): # args = [(type I, inp I), (type II, inp II), ...]
        z = dict(args[:])
        return sum([i(z(type(i))) for i in self.array])
    
    def __add__(self, other):
        return Add([self, other])
    
    def __neg__(self):
        return Mul(self.array[:] + (-1))
    
    def __sub__(self, other):
        return self + (-other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Mul(self.array[:] + [other])
        return Mul(self.array[:] + other.array[:])

    def __truediv__(self, other):
        pass   
    __rmul__ = __mul__
    __radd__ = __add__

    def diff(self):
        array = []
        for i in range(len(self.array[:])):
            if i < len(self.array) - 1:
                array.append(Mul([self.array[i].diff()] + self.array[:i] + self.array[i+1:]))
            else:
                array.append(Mul([self.array[i].diff()] + self.array[:i]))
        
        return Add(array[:])

class sin:
    def __init__(self, inp):
        self.input = inp
    