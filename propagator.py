class Propagator:
    def __init__(self, people, rate=0.0) -> None:
        self.people = people
        self.rate = rate

    def step(self):
        if self.rate > 0.5:
            for person in self.people:
                person.infected = True
