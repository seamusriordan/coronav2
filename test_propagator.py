from random import random
from unittest import TestCase, mock

from person import Person
from propagator import Propagator


class Test(TestCase):
    two_in_contact = None

    def setUp(self) -> None:
        self.two_in_contact = [Person(), Person()]
        self.two_in_contact[0].contacts.append(self.two_in_contact[1])
        self.two_in_contact[1].contacts.append(self.two_in_contact[0])

    def test_step_with_two_in_contact_and_zero_rate_does_nothing(self):
        propagator = Propagator(self.two_in_contact, rate=0.0)

        propagator.step()

        self.assertFalse(self.two_in_contact[0].infected)
        self.assertFalse(self.two_in_contact[1].infected)

    def test_step_one_infected_unity_rate_infects_other(self):
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=1.0)

        propagator.step()

        self.assertTrue(self.two_in_contact[1].infected)

    @mock.patch('random.random')
    def test_step_half_rate_infects_other_with_rng_zero(self, mock_random):
        mock_random.return_value = 0.0
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=0.5)

        propagator.step()

        self.assertTrue(self.two_in_contact[1].infected)

    def test_none_in_contact_do_not_infect(self):
        people = [Person(), Person()]
        people[0].infected = True
        propagator = Propagator(people, rate=1.0)

        propagator.step()

        self.assertFalse(people[1].infected)

    def test_infected_recover_after_infection_length_steps_of_2(self):
        infected_person = Person()
        infected_person.infected = True
        propagator = Propagator([infected_person], infection_length=2)

        propagator.step()
        propagator.step()

        self.assertFalse(infected_person.infected)

    def test_infected_given_infection_length_3_is_still_infected_after_2_steps(self):
        infected_person = Person()
        infected_person.infected = True
        propagator = Propagator([infected_person], infection_length=3)

        propagator.step()
        propagator.step()

        self.assertTrue(infected_person.infected)

    def test_recovered_do_not_get_reinfected(self):
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=1.0, infection_length=1)

        propagator.step()
        propagator.step()

        self.assertFalse(self.two_in_contact[0].infected)

    def test_all_infected_die_with_mortality_1(self):
        person = Person()
        person.infected = True
        propagator = Propagator([person], mortality=1.0)

        propagator.step()

        self.assertTrue(person.dead)

    def test_not_infected_with_mortality_1_dont_die(self):
        person = Person()
        propagator = Propagator([person], mortality=1.0)

        propagator.step()

        self.assertFalse(person.dead)

    @mock.patch("random.random")
    def test_all_infected_die_with_mortality_one_tenth_and_rng_0(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], mortality=0.1)

        propagator.step()

        self.assertTrue(person.dead)

    @mock.patch("random.random")
    def test_those_that_die_are_not_considered_infected(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], mortality=1.0)

        propagator.step()

        self.assertFalse(person.infected)

    @mock.patch("random.random")
    def test_the_dead_do_not_infect(self, mock_random):
        mock_random.return_value = 0.0
        self.two_in_contact[0].dead = True
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, mortality=1.0, rate=1.0)

        propagator.step()

        self.assertFalse(self.two_in_contact[1].infected)

    @mock.patch("random.random")
    def test_those_that_die_do_not_recover(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], mortality=1.0, infection_length=1)

        propagator.step()

        self.assertFalse(person.recovered)
