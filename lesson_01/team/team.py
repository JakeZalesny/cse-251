"""
Course: CSE 251 
Lesson: L01 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review and follow the team activity instructions (INSTRUCTIONS.md)
"""

from datetime import datetime, timedelta
import threading

# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def is_prime(n):
    global numbers_processed
    numbers_processed += 1

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

def do_threading(start, range_count):
    global prime_count
    for i in range(start, range_count):
        if is_prime(i):
            prime_count += 1
            print(i, end=', ', flush=True)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    threads = []
    start = 10000000000
    range_count = 100000
    for i in range(1):
        # divide the range up into into each CPU core, core 1 gets range 1-100, 
        threads.append(threading.Thread(target=do_threading, args=(start, range_count)))
    
    for i in threads:
        i.start()
    
    for i in threads:
        i.join()

    # TODO 3) change the program to divide the for loop into 10 threads
    second_threads = []
    start = 0
    range_count = 10000
    for i in range(10):
        second_threads.append(threading.Thread(target=do_threading, args=(start, range_count)))
        start = range_count + 1
        range_count += 1000

    for thread in second_threads:
        thread.start()
    
    for thread in second_threads:
        thread.join()

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')

