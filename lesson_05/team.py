"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: Jake Zalesny

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def read_thread(list_of_primes, queue_to_process, data_is_available, process_lock, filename:str):
    with open(filename, "r") as file:
        for line in file:
            num = int(line)
            process_lock.acquire()
            queue_to_process.put(num)
            data_is_available.release()
            process_lock.release()
    
    for _ in range(PRIME_PROCESS_COUNT):
        queue_to_process.put(None)
        data_is_available.release()
    process_lock.release()
# TODO create prime_process function
def prime_process(p_id, list_of_primes, queue_to_process, data_is_available, process_lock):
    while True:
        data_is_available.acquire()
        process_lock.acquire()
        num = queue_to_process.get()
        process_lock.release()

        if num == None:
            return

        if is_prime(num):
            print(f"Prime found: {num}; {p_id}")
            list_of_primes.append(num)


def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    # Create the data file for this demo if it does not already exist.
    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    list_of_primes = mp.Manager().list()
    queue_to_process = mp.Queue()
    data_available = mp.Semaphore(0)
    process_lock = mp.Lock()

    # TODO create reading thread
    reader = threading.Thread(target=read_thread, args=(list_of_primes, queue_to_process, data_available, process_lock, filename))
    # TODO create prime processes
    processes = []
    for i in range(PRIME_PROCESS_COUNT):
        processes.append(mp.Process(target=prime_process, args=(i, list_of_primes, queue_to_process, data_available, process_lock)))
    # TODO Start them all
    reader.start()
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()

    # TODO wait for them to complete

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(list_of_primes)} found:')
    for prime in list_of_primes:
        print(prime)


if __name__ == '__main__':
    main()
