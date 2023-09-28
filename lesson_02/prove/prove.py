"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0 


# TODO Add your threaded class definition here
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
            global call_count 
            call_count += 1
        else:
            print('Response =', response.status_code)
        # self.lock.release()



# TODO Add any functions you need here
class Star_Wars:
    def __init__(self) -> None:
        self.results = {}
        self.film_link = None
        self.thread = None
        self.film_data = None
    
    def get_top_api(self):
        self.thread = Request_thread(TOP_API_URL)
        self.thread.start()
        self.thread.join()
    
    def get_film_data(self, film_number:int) -> dict:
      self.film_link = self.thread.results["films"]
      self.film_link = rf"{self.film_link}{film_number}"
      self.thread = Request_thread(self.film_link)
      self.thread.start()
      self.thread.join()
      self.film_data = self.thread.results
      return self.film_data
    
    def get_object(self, object:str):
        objects_container = self.film_data[object]
        objects = []
        
        threads = []

        for object in objects_container:
            self.thread = Request_thread(object)
            threads.append(self.thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
            objects.append(thread.results["name"])
        
        return objects
        
      



def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    star_wars = Star_Wars()
    star_wars.get_top_api()
    # TODO Retrieve Details on film 6
    film_data = star_wars.get_film_data(6)
    
    characters = star_wars.get_object("characters")
    character_str = ", ".join(characters)
    
    planets = star_wars.get_object("planets")
    planet_str = ", ".join(planets)

    starships = star_wars.get_object("starships")
    starship_str = ", ".join(starships)

    vehicles = star_wars.get_object("vehicles")
    vehicles_str = ", ".join(vehicles)

    species = star_wars.get_object("species")
    species_str = ", ".join(species)

    log.write(f"Title   : {film_data['title']}")
    log.write(f"Director: {film_data['director']}")
    log.write(f"Producer: {film_data['producer']}")
    log.write(f"Released:{film_data['release_date']}")
    
    log.write("")
    log.write(f"Characters: {len(characters)}")
    log.write(f"{character_str}, ")
    
    log.write("")
    log.write(f"Planets: {len(planets)}")
    log.write(f"{planet_str}, ")
    
    log.write("")
    log.write(f"Starships: {len(starships)}")
    log.write(f"{starship_str}, ")
    
    log.write("")
    log.write(f"Vehicles: {len(vehicles)}")
    log.write(f"{vehicles_str}, ")
    
    log.write("")
    log.write(f"Species: {len(species)}")
    log.write("")
    log.write(f"{species_str}, ")
    
    log.write("")

    # TODO Display results
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()