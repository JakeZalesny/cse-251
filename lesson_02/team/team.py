"""
Course: CSE 251 
Lesson: L02 Team Activity
File:   team.py
Author: Jake Zalesny

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
import threading
from typing import Any
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, url):
        super().__init__()
        self.url = url
        # self.lock = threading.Lock()
        self.results = {}
    
    def run(self):
        # self.lock.acquire()
        response = requests.get(self.url)
        if response.status_code == 200:
            self.results = response.json()
        else:
            print('Response = ', response.status_code)
        # self.lock.release()

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # print('Reshuffle Deck')
        # TODO - add call to reshuffle
        reshuffle_url = rf"https://deckofcardsapi.com/api/deck/{self.id}/shuffle/"
        thread1 = Request_thread(url=reshuffle_url)
        thread1.start()
        thread1.join()
        self.remaining = thread1.results["remaining"]



    def draw_card(self):
        # TODO add call to get a card
        card_url = rf"https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1"
        thread2 = Request_thread(url=card_url)
        thread2.start()
        thread2.join()
        if thread2.results != {}:
            self.remaining = thread2.results['remaining']
            return thread2.results['cards'][0]['code']
        else:
            return '' 

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'odbkqrjou9p0'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<
