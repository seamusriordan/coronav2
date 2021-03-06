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

        propagator.step_n(2)

        self.assertFalse(infected_person.infected)

    def test_infected_given_infection_length_3_is_still_infected_after_2_steps(self):
        infected_person = Person()
        infected_person.infected = True
        propagator = Propagator([infected_person], infection_length=3)

        propagator.step_n(2)

        self.assertTrue(infected_person.infected)

    def test_recovered_do_not_get_reinfected(self):
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=1.0, infection_length=1)

        propagator.step_n(2)

        self.assertFalse(self.two_in_contact[0].infected)

    def test_all_infected_die_with_mortality_1(self):
        person = Person()
        person.infected = True
        propagator = Propagator([person], daily_mortality=1.0)

        propagator.step()

        self.assertTrue(person.dead)

    def test_not_infected_with_mortality_1_dont_die(self):
        person = Person()
        propagator = Propagator([person], daily_mortality=1.0)

        propagator.step()

        self.assertFalse(person.dead)

    @mock.patch("random.random")
    def test_all_infected_die_with_mortality_one_tenth_and_rng_0(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], daily_mortality=0.1)

        propagator.step()

        self.assertTrue(person.dead)

    @mock.patch("random.random")
    def test_those_that_die_are_not_considered_infected(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], daily_mortality=1.0)

        propagator.step()

        self.assertFalse(person.infected)

    @mock.patch("random.random")
    def test_the_dead_do_not_infect(self, mock_random):
        mock_random.return_value = 0.0
        self.two_in_contact[0].dead = True
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, daily_mortality=1.0, rate=1.0)

        propagator.step()

        self.assertFalse(self.two_in_contact[1].infected)

    @mock.patch("random.random")
    def test_those_that_die_do_not_recover(self, mock_random):
        mock_random.return_value = 0.0
        person = Person()
        person.infected = True
        propagator = Propagator([person], daily_mortality=1.0, infection_length=1)

        propagator.step()

        self.assertFalse(person.recovered)

    def test_results_has_length_of_steps_with_one_step(self):
        propagator = Propagator(self.two_in_contact)

        propagator.step()

        self.assertEqual(1, len(propagator.results.day))

    def test_results_has_length_of_steps_with_three_steps(self):
        propagator = Propagator(self.two_in_contact)

        n_steps = 3
        propagator.step_n(n_steps)

        self.assertEqual(n_steps, len(propagator.results.day))

    def test_results_days_are_consecutive_for_four_days(self):
        propagator = Propagator(self.two_in_contact)

        n_steps = 4
        propagator.step_n(n_steps)

        self.assertEqual([0, 1, 2, 3], propagator.results.day)

    def test_results_infected_count_infected(self):
        self.two_in_contact[0].infected = True
        self.two_in_contact[1].infected = True

        propagator = Propagator(self.two_in_contact, infection_length=1)

        propagator.step_n(2)

        self.assertEqual([2, 0], propagator.results.infected_count)

    def test_results_recovered_count_recovered_with_two(self):
        self.two_in_contact[0].infected = True
        self.two_in_contact[1].infected = True

        propagator = Propagator(self.two_in_contact, infection_length=1, daily_mortality=0)

        propagator.step_n(2)

        self.assertEqual([0, 2], propagator.results.recovered_count)

    def test_results_recovered_count_recovered(self):
        self.two_in_contact[0].infected = True

        propagator = Propagator(self.two_in_contact, infection_length=1, daily_mortality=0)

        propagator.step_n(2)

        self.assertEqual([0, 1], propagator.results.recovered_count)

    def test_results_dead_count_dead(self):
        self.two_in_contact[0].infected = True
        self.two_in_contact[1].dead = True

        propagator = Propagator(self.two_in_contact, infection_length=10, daily_mortality=1.0)

        propagator.step_n(2)

        self.assertEqual([1, 2], propagator.results.dead_count)
