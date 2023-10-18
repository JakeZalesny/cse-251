"""
Course: CSE 251 
Lesson: L04 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Practice concepts of Queues, Locks, and Semaphores.

Instructions:

- Review instructions in Canvas.

Question:

- Is the Python Queue thread safe? (https://en.wikipedia.org/wiki/Thread_safety)
"""

import threading
import queue
import requests
import json
from cse251 import Log

# Include cse 251 common Python files
from cse251 import *

URL = "http://127.0.0.1:8790"
RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(log, q:queue.Queue(), semaphore):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
            semaphore.acquire()
            url = q.get()

            if url == NO_MORE_VALUES:
                return
        
        # TODO process the value retrieved from the queue
            response = requests.get(url=url)

        # TODO make Internet call to get characters name and log it
            if response.status_code == 200: 
                result = response.json()
                log.write(result['name'])
            else:
                log.write("NAME NOT FOUND") 


def file_reader(log, file, q:queue.Queue(), semaphore): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open("urls.txt", "r") as file:
        for line in file: 
            q.put(line.strip())
            semaphore.release() #Everything starts in a sleep, then when you release the semaphore it makes them start. It's using the semaphore in reverse
    
    log.write('Finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    q.put(NO_MORE_VALUES)
    semaphore.release()


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)
    urls_to_be_processed = threading.Semaphore(0) #nothing to process right now. 
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader_thread = threading.Thread(target=file_reader, args=(log,"urls.txt", q, urls_to_be_processed))
    threads = []
    for _ in range(RETRIEVE_THREADS):
        threads.append(threading.Thread(target=retrieve_thread, args=(log, q, urls_to_be_processed)))
    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader\
    
    for thread in threads:
        thread.start()
    
    reader_thread.start()

    
    # TODO Wait for them to finish - The order doesn't matter
    reader_thread.join()
    for thread in threads:
        thread.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()



