import numpy as np
from multiprocessing import Pool
from time import sleep
from parallelize_native import smart_parallelize


def func(x, y):
    
    x = np.array(x)
    y = np.array(y)
    return x+y


def f3(x, y, z):
    
    x = np.array(x)
    y = np.array(y)
    return x+y+z

def f2(x):
    y = 1
    
    x = np.array(x)
    y = np.array(y)
    return x+y

def f4(x):
    y = 1
    
    x = np.array(x)
    y = np.array(y)
    return x,y

def f5(x, y, z, w):

    test = lambda x: x
    c = test(x)
    
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    w = np.array(w)
    return x+y+z+w

def test_inner():
    def inner(x):
        return x
    x = list(np.ones((20,2)))
    out = smart_parallelize(inner, 1, x)
    return out

if __name__ == "__main__":
    import timeit

    
    x = list(np.ones((20,2)))
    y = list(np.ones((20,2))*3)
    z = 2
    start  = timeit.default_timer()

    a1 = smart_parallelize(f2, 1, x)
    answer = smart_parallelize(func, 2, x, y)
    a3 = smart_parallelize(f3, 2, x, y, z)
    a4 = smart_parallelize(f4, 1, x)
    a5 = smart_parallelize(f5, 1, x, z, z, z)
    
    stop  = timeit.default_timer()
    print(stop - start)
    print(answer)

    # for i,x_val in enumerate(x):
    #     print(func(x_val))