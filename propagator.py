from random import random

from person import Person


class Propagator:
    def __init__(self, people: [Person], rate=0.0, infection_length=10):
        self.people: [Person] = people
        self.rate = rate
        self.infection_length = infection_length

    def step(self):
        infector: Person
        for infector in self.people:
            self.propagate_infectors(infector)
            self.increment_infection_time(infector)
            self.recover(infector)

    @staticmethod
    def increment_infection_time(infector):
        if infector.infected:
            infector.time_infected += 1

    def recover(self, infector):
        if infector.infected and infector.time_infected >= self.infection_length:
            infector.infected = False
            infector.recovered = True

    def propagate_infectors(self, infector):
        if infector.infected:
            self.propagate_infection(infector)

    def propagate_infection(self, infector: Person):
        infectee: Person
        for infectee in infector.contacts:
            if not infectee.recovered and self.rate > random():
                infectee.infected = True
