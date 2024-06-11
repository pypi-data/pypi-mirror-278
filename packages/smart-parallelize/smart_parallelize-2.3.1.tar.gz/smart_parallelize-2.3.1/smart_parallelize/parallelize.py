# from functools import wraps

# import numpy as np
# from ray.exceptions import RaySystemError
# from ray import available_resources, init, remote, get, put


# def get_mem_func():
#     try:
#         MEMORY = available_resources()['memory']
#     except RaySystemError:
#         init()
#         MEMORY = available_resources()['memory']
#     try:
#         CPUS = available_resources()['CPU']
#         MEM_PER_WORKER = (MEMORY / CPUS) * 0.8
#     except KeyError:
#         # get number of cores
#         import multiprocessing
#         CPUS = multiprocessing.cpu_count()
#         MEM_PER_WORKER = (MEMORY / CPUS) * 0.8
#     MEMORY = int(MEMORY)
#     CPUS   = int(CPUS)
#     MEM_PER_WORKER = int(MEM_PER_WORKER)
#     return MEMORY, CPUS, MEM_PER_WORKER

# try:
# 	MEMORY, CPUS, MEM_PER_WORKER = get_mem_func()
# except RaySystemError:
# 	MEMORY, CPUS, MEM_PER_WORKER = get_mem_func()


# def smart_parallelize(args2parallelize=1):
#     def decorator(function):
#         @wraps(function)
#         def wrapper(**kwargs):
#             @remote(memory=MEM_PER_WORKER)
#             def get_results(**kwargs):
#                 par_args = list(kwargs.keys())[:args2parallelize]
#                 other_args = list(kwargs.keys())[args2parallelize:]
#                 data_par_args = [kwargs[i] for i in par_args]

#                 results = []
#                 for i, _ in enumerate(data_par_args[0]):
#                     kwargs_0 = kwargs.copy()
#                     for j, arg in enumerate(par_args):
#                         kwargs_0[arg] = data_par_args[j][i]
#                     for k, arg in enumerate(other_args):
#                         kwargs_0[arg] = kwargs[arg]
#                     r = function(**kwargs_0)
#                     results.append(r)
#                 return results
            
#             par_args = list(kwargs.keys())[:args2parallelize]
#             other_args = list(kwargs.keys())[args2parallelize:]
#             arg2parallelize_unsplit = [kwargs[i] for i in par_args]

#             # split into CPUS chunks
#             split_args = [np.array_split(i, CPUS) for i in arg2parallelize_unsplit]

#             workers = []
#             for i in range(CPUS):
#                 inp_args = {}
#                 for j, _ in enumerate(par_args):
#                     inp_args[par_args[j]] = split_args[j][i]
                
#                 for k, _ in enumerate(other_args):
#                     inp_args[other_args[k]] = kwargs[other_args[k]]
#                 workers.append(get_results.remote(**inp_args))
            
#             test_inp = {}
#             for j, _ in enumerate(par_args):
#                 test_inp[par_args[j]] = arg2parallelize_unsplit[j][0]
#             for k, _ in enumerate(other_args):
#                 test_inp[other_args[k]] = kwargs[other_args[k]]

#             output = function(**test_inp)
#             if not isinstance(output, list) and not isinstance(output, tuple):
#                 num_outputs = 1
#             else:
#                 num_outputs = len(output)

#             retval = get(workers)

#             # retval = retval.reshape(len(arg2parallelize_unsplit[0]), num_outputs)

#             retval = [j for i in retval for j in i]

#             if num_outputs != 1:
#                 outputs = []
#                 for i in range(num_outputs):
#                     outputs.append([])
#                 for i, _ in enumerate(retval):
#                     for j, _ in enumerate(retval[i]):
#                         outputs[j].append(retval[i][j])
#                 retval = outputs
#                 for i in range(num_outputs):
#                     outputs[i] = np.array(outputs[i])
#             else:
#                 retval = np.array(retval)
#             return retval
#         return wrapper
#     return decorator


# if __name__ == "__main__":
#     import timeit

#     @smart_parallelize(args2parallelize=1)
#     def func(x, y):
#         return x
    
#     x = np.ones((31,2))
#     # y = np.ones((30,))*2
#     y = 2
#     start  = timeit.default_timer()
#     answer = func(x=x, y=y)
#     stop  = timeit.default_timer()
#     print(stop - start)
#     print(answer)
