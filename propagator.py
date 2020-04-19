import random

from person import Person


class Propagator:
    def __init__(self, people: [Person], rate=0.0, infection_length=10, daily_mortality=0.0):
        self.people: [Person] = people
        self.rate = rate
        self.infection_length = infection_length
        self.daily_mortality = daily_mortality

        self.results: Results = Results()
        self.step_index: int = 0

    def step_n(self, n_steps):
        for _ in range(n_steps):
            self.step()

    def step(self):
        self.count_results()
        self.step_index += 1
        for person in self.people:
            if person.infected:
                self.step_infection(person)

    def step_infection(self, infected):
        self.process_death(infected)
        self.propagate_infectors(infected)
        self.increment_infection_time(infected)
        self.recover(infected)

    def process_death(self, infected: Person):
        if self.daily_mortality > random.random():
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

    def count_results(self):
        n_infected = self.count_infected(self.people)
        n_dead = self.count_dead(self.people)
        n_recovered = self.count_recovered(self.people)

        self.results.day.append(self.step_index)
        self.results.infected_count.append(n_infected)
        self.results.dead_count.append(n_dead)
        self.results.recovered_count.append(n_recovered)

    @staticmethod
    def count_infected(people: [Person]) -> int:
        return sum(map((lambda x: 1 if x.infected else 0), people))

    @staticmethod
    def count_dead(people: [Person]) -> int:
        return sum(map((lambda x: 1 if x.dead else 0), people))

    @staticmethod
    def count_recovered(people: [Person]) -> int:
        return sum(map((lambda x: 1 if x.recovered else 0), people))


class Results:
    def __init__(self) -> None:
        self.day: [int] = []
        self.infected_count: [int] = []
        self.dead_count: [int] = []
        self.recovered_count: [int] = []
