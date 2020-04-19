from random import random

from person import Person


class Propagator:
    def __init__(self, people: [Person], rate=0.0, infection_length=10):
        self.people: [Person] = people
        self.rate = rate

    def step(self):
        infector: Person
        for infector in self.people:
            self.propagate_infectors(infector)
            infector.time_infected += 1
            if infector.infected and infector.time_infected >= 2:
                infector.infected = False

    def propagate_infectors(self, infector):
        if infector.infected:
            self.propagate_infection(infector)

    def propagate_infection(self, infector: Person):
        infectee: Person
        for infectee in infector.contacts:
            if self.rate > random():
                infectee.infected = True
