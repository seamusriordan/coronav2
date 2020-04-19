import random

from person import Person


class Propagator:
    def __init__(self, people: [Person], rate=0.0, infection_length=10, mortality=0.0):
        self.people: [Person] = people
        self.rate = rate
        self.infection_length = infection_length
        self.mortality = mortality

    def step(self):
        for person in self.people:
            if person.infected:
                self.step_infection(person)

    def step_infection(self, infected):
        self.process_death(infected)
        self.propagate_infectors(infected)
        self.increment_infection_time(infected)
        self.recover(infected)

    def process_death(self, infected: Person):
        if self.mortality > random.random():
            infected.dead = True
            infected.infected = False

    @staticmethod
    def increment_infection_time(infected: Person):
        infected.time_infected += 1

    def recover(self, infected):
        if not infected.dead and infected.time_infected >= self.infection_length:
            infected.infected = False
            infected.recovered = True

    def propagate_infectors(self, infector: Person):
        if not infector.dead:
            self.propagate_infection(infector)

    def propagate_infection(self, infector: Person):
        infectee: Person
        for infectee in infector.contacts:
            if not infectee.recovered and self.rate > random.random():
                infectee.infected = True
