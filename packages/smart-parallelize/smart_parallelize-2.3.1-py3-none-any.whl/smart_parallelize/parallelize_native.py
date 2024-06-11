import numpy as np
# from multiprocessing import Pool
# from pathos.parallel import ParallelPool
from pathos.multiprocessing import Pool
from time import sleep


# print('testing')
# sleep(1)

def smart_parallelize(func, args2parallelize, *args):
    args2par = list(args[:args2parallelize])
    args2par2 = []
    for i,a in enumerate(args2par[0]):
        c = []
        for i in range(args2parallelize):
            c.append(a)
        args2par2.append(tuple(c))
    args2par = args2par2
    argsnotpar = list(([args[args2parallelize:]]))*len(args2par)

    if len(argsnotpar[0]) != 0:
        inputs = [a+argsnotpar[i] for i, a in enumerate(args2par)]
    else:
        inputs = args2par

    with Pool() as p:
        out = p.starmap(func, inputs)
    
    if isinstance(out[0], list) or isinstance(out[0], np.ndarray):
        num_outs = 1
        out = out
        return out
    else:
        num_outs = len(out[0])
    out_new = []
    for i in range(num_outs):
        out_new.append([])
    for i, _ in enumerate(out):
        for j in range(num_outs):
            out_new[j].append(np.array(out[i][j]))
    for i in range(num_outs):
        out_new[i] = out_new[i]
    out = tuple(out_new)
    return out

def func(x, y):
    # y = 1
    sleep(1)
    x = np.array(x)
    y = np.array(y)

    # print(x, y)
    return x+y

def f3(x, y, z):
    # y = 1
    sleep(1)
    x = np.array(x)
    y = np.array(y)

    # print(x, y)
    return x+y+z

def f2(x):
    y = 1
    sleep(1)
    x = np.array(x)
    y = np.array(y)

    return x+y

def f4(x):
    y = 1
    sleep(1)
    x = np.array(x)
    y = np.array(y)

    return x,y


if __name__ == "__main__":
    import timeit

    
    x = list(np.ones((20,2)))
    y = list(np.ones((20,2))*3)
    z = 2
    start  = timeit.default_timer()

    # a1 = smart_parallelize(f2, 1, x)
    # answer = smart_parallelize(func, 2, x, y)
    # a3 = smart_parallelize(f3, 2, x, y, z)
    # a4 = smart_parallelize(f4, 1, x)
    a5 = smart_parallelize(f4, 1, np.ones((7,1)).flatten())
    
    stop  = timeit.default_timer()
    print(stop - start)
    # print(answer)

    # for i,x_val in enumerate(x):
    #     print(func(x_val))