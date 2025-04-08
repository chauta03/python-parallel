import numpy as np
import pandas as pd
import util 
def slow_appends(arr):
    l = []
    for x in arr:
        l.append(x ** 101)
    return l

def faster_list_compre(arr):
    return [i ** 101 for i in arr]

def fast_numpy(arr):
    return np.array(arr) ** 101

def make_data1(size=1000):
    np.random.seed(4)
    array1 = np.random.rand(size, 1)  # np.array
    df1 = pd.DataFrame(array1)  # pd.DataFrame
    return df1

def main():
    input = make_data1()
    arr = input[0].to_numpy()
    
    funcs = [slow_appends, faster_list_compre]
    args = [[arr], [arr]]
    names = ["slow_appends", "faster_list_compre"]
    reps = 10
    timings, data = util.time_funcs(funcs, args, names, reps)
    util.print_time_results(timings, len(arr))


if __name__ == "__main__":
    main()