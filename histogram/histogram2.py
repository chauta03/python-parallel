import time
import random
from prettytable import PrettyTable
from typing import List
from multiprocessing.pool import ThreadPool
import concurrent.futures
import os
import numpy as np
import multiprocessing as mp
from functools import partial

BINS = 10
MAX_THREADS = 512
MAX_SIZE = 10 ** 7

def histogram_seq(max_exp):
    n = 10
    max_size = 10 ** max_exp
    seq_duration = []

    print("Processing histogram sequentially...")

    while n <= max_size:
        histogram = [0 for _ in range(BINS)]

        print("calculating histogram for " + str(n) + " elements")
        data = [0 for _ in range(n)]

        # start timing
        start = time.time()

        # Geerate random data points from 0 to 9
        for i in range(n):
            data[i] = np.random.randint(0, 9)
            histogram[data[i]] += 1
        
        # stop timing
        stop = time.time()
        # get duration
        duration = stop - start
        seq_duration.append(round(duration, 8))
        n *= 10
        
    
    print()
    print("Done!" + '\n' * 2  + "Printing results: " + '\n')

    print(['n (size)', 'time (s)'])
    for i in range(max_exp):
        print(["10^" + str(i+1), seq_duration[i]])


def task(t_histogram, chunk):
    for i in range(len(chunk)):
        t_point = np.random.randint(0, 9) % 10
        chunk[i] = t_point
        t_histogram[chunk[i]] += 1

def run_parallel_histogram():
    n = 10
    threads = 256

    while n <= MAX_SIZE:
        t_histogram = [0 for _ in range(BINS)]

        data = [0 for _ in range(n)]
        
        chunks = np.array_split(data, threads)

        task_with_constant = partial(task, t_histogram)

        pool = ThreadPool(processes=threads)


        start = time.time()

        # run parallel
        for result in pool.map(task_with_constant, chunks):
            continue

        duration = time.time() - start
        pool.close()
        round(duration, 8)

        print(n, duration)
        n *= 10


def run_parallel_histogram2():
    n = 10
    process_pool = 8

    while n <= MAX_SIZE:
        t_histogram = [0 for _ in range(BINS)]

        data = [0 for _ in range(n)]

        chunks = np.array_split(data, process_pool)

        task_with_constant = partial(task, t_histogram)


        start = time.time()

        # run parallel
        with mp.Pool(process_pool) as pool:
            results = pool.map(task_with_constant, chunks)

        duration = time.time() - start
        round(duration, 8)

        print(n, duration)
        n *= 10

def main():
 
    n = 10
    max_exp = 7

    # histogram_seq( max_exp)

    run_parallel_histogram2()

    # histogram_para_process()


if __name__ == "__main__":
    main()