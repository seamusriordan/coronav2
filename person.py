class Person:
    def __init__(self):
        self.dead = False
        self.time_infected = 0
        self.infected = False
        self.recovered = False
        self.contacts: [Person] = []
