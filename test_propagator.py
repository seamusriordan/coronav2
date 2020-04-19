from unittest import TestCase

from propagator import Propagator


class Test(TestCase):
    def testInitSetsUpNPeopleWith5People(self):
        n_people = 5
        propagator = Propagator(n_people)

        self.assertEqual(len(propagator.people), n_people)

    def testInitSetsUpNPeopleWith20People(self):
        n_people = 20
        propagator = Propagator(n_people)

        self.assertEqual(len(propagator.people), n_people)
