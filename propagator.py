from random import random

from person import Person


class Propagator:
    def __init__(self, people: [Person], rate=0.0):
        self.people: [Person] = people
        self.rate = rate

    def step(self):
        infector: Person
        for infector in self.people:
            if infector.infected:
                self.propagate_infection(infector)

    def propagate_infection(self, infector: Person):
        infectee: Person
        for infectee in infector.contacts:
            if self.rate > random():
                infectee.infected = True
