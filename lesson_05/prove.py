"""
Course: CSE 251 
Lesson: L05 Prove
File:   prove.py
Author: Jake Zalesny

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Global Constants.
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, fac_semaphore, deal_semaphore, queue, barrier, factory_stats, dealer_count):
        super().__init__()
        self.cars_to_produce = random.randint(200, 300) # DO NOT change
        self.queue = queue
        self.fac_semaphore = fac_semaphore
        self.deal_semaphore = deal_semaphore
        self.barrier = barrier
        self.factory_stats = factory_stats
        self.dealer_count = dealer_count


    def run(self):
        # TODO produce the cars, the send them to the dealerships
        # TODO wait until all of the factories are finished producing cars
        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        for i in range(self.cars_to_produce):
            # TODO Add your code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """
            self.fac_semaphore.acquire()
            self.queue.put(Car())
            # self.factory_stats[self.queue.size()] += 1
            self.deal_semaphore.release()

        # signal the dealer that there there are not more cars
        wait_num = self.barrier.wait()
        if wait_num == 0: 
            for i in range(self.dealer_count):
                self.fac_semaphore.acquire()
                self.queue.put('No More Cars!')
                self.deal_semaphore.release() 



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, fac_semaphore, deal_semaphore, dealer_stats):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        super().__init__()
        
        self.queue = queue
        self.fac_semaphore = fac_semaphore
        self.deal_semaphore = deal_semaphore
        self.queue_stats = dealer_stats

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.deal_semaphore.acquire()
            car = self.queue.get()
            if car == 'No More Cars!':
                return False
            # self.queue_stats[self.queue.size()] += 1
            self.fac_semaphore.release()
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s) if needed
    fac_semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    deal_semaphore = threading.Semaphore(0)
    # TODO Create queue
    queue = Queue251()
    # TODO Create lock(s) if needed
    # TODO Create barrier
    barrier = mp.Barrier(factory_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    factory_stats = list([0] * factory_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = []
    dealers = []

    for _ in range(factory_count):
        factories.append(Factory(fac_semaphore=fac_semaphore, deal_semaphore=deal_semaphore, queue=queue, barrier=barrier, factory_stats=factory_stats, dealer_count=dealer_count))
    
    # TODO create your dealerships
    for _ in range(dealer_count):
        dealers.append(Dealer(fac_semaphore=fac_semaphore, deal_semaphore=deal_semaphore, queue=queue, dealer_stats=dealer_stats))

    log.start_timer()

    # TODO Start all dealerships
    for dealer in dealers:
        dealer.start()
    # TODO Start all factories
    for factory in factories:
        factory.start()

    # TODO Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()
    
    for dealer in dealers:
        dealer.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created.')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)

