import time
import random
from prettytable import PrettyTable
from typing import List
from multiprocessing.pool import ThreadPool
import concurrent.futures
import os

BINS = 10
MAX_THREADS = 512
n = 10
max_exp = 7
max_size = 10 ** max_exp
data = [0 for _ in range(max_size)]

def histogram_seq():
    n = 10
    max_size = 10 ** max_exp
    seq_duration = []

    print("Processing histogram sequentially...")

    while n <= max_size:
        histogram = [0 for _ in range(BINS)]

        print("calculating histogram for " + str(n) + " elements")

        # start timing
        start = time.time()

        # Geerate random data points from 0 to 9
        for i in range(n):
            data[i] = random.randrange(0, 9)

        # Organize data by placing data points into corresponding bins
        for i in range(n):
            histogram[data[i]] += 1
        
        # stop timing
        stop = time.time()
        # get duration
        duration = stop - start
        seq_duration.append(duration)
        n *= 10
        
    
    print()
    print("Done!" + '\n' * 2  + "Printing results: " + '\n')

    t = PrettyTable(['n (size)', 'time (s)'])
    for i in range(max_exp):
        t.add_row(["10^" + str(i+1), seq_duration[i]])
    
    t.align = "l"
    print(t)
    return



# PARALLEL IMPLEMENTATION

def task(n):
        t_histogram = [0 for _ in range(BINS)]

        start = time.time()

        for i in range(n):
            data[i] = random.randrange(0, 9)

        for i in range(n):
            t_histogram[data[i]] += 1
        
        end = time.time()

        return round(end - start, 8)

def histogram_para_thread():
    max_size = 10 ** max_exp
    par_durations = [[0 for _ in range(10)] for _ in range(9)]

    threads = 1
    col = 0

    print("Processing histogram in  parallel using ThreadPool ...")

    while threads <= MAX_THREADS:
        print("  Using " + str(threads) + " threads")

        row = 0
        
        items = [10 ** i for i in range(1, max_exp + 1)]

        pool = ThreadPool(processes=threads)

        for result in pool.map(task, items):
            par_durations[row][col] = result
            row += 1
        
        threads *= 2
        col += 1

    header = ["n (size)"]

    for i in range(10):
        x = 2 ** i
        header.append("T=" +  str(x) + " (s)")
        
    t = PrettyTable(header)
    

    for i in range(max_exp):
        rowRes = ["10^" + str(i+1)] + par_durations[i]
        t.add_row(rowRes)
    
    t.align = "l"
    print(t)

    return



# do the same function using ProcessPoolExecutor instead of ThreadPool
def histogram_para_process():
    max_size = 10 ** max_exp
    n = 10
    par_durations = [[0 for _ in range(10)] for _ in range(9)]
    n_cores = os.cpu_count()

    threads = 1
    col = 0

    print("Processing histogram in  parallel using ProcessPoolExecutor ...")

    while threads <= MAX_THREADS:
        print("  Using " + str(threads) + " threads")

        row = 0
        
        items = [10 ** i for i in range(1, max_exp + 1)]
        step = len(items) // n_cores


        with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
            # divide array items into chunks and process each chunk in parallel
            if step != 0:
                chunks = [items[i:i+step] for i in range(0, len(items), step)]

                chunks[-1].extend(items[len(chunks) * step:]) 
            else:
                chunks = [[i] for i in items]
            
            for result in executor.map(task, chunks):
                par_durations[row][col] = result
                row += 1
        
        threads *= 2
        col += 1

    header = ["n (size)"]

    for i in range(10):
        x = 2 ** i
        header.append("T=" +  str(x) + " (s)")
        
    t = PrettyTable(header)
    

    for i in range(max_exp):
        rowRes = ["10^" + str(i+1)] + par_durations[i]
        t.add_row(rowRes)
    
    t.align = "l"
    print(t)

    return

def main():

    # histogram_seq()

    histogram_para_thread()

    histogram_para_process()


if __name__ == "__main__":
    main()






