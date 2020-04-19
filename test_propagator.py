from unittest import TestCase, mock

from person import Person
from propagator import Propagator


class Test(TestCase):
    two_in_contact = None

    def setUp(self) -> None:
        self.two_in_contact = [Person(), Person()]
        self.two_in_contact[0].contacts.append(self.two_in_contact[1])
        self.two_in_contact[1].contacts.append(self.two_in_contact[0])

    def test_propagator_step_with_two_in_contact_and_zero_rate_does_nothing(self):
        propagator = Propagator(self.two_in_contact, rate=0.0)

        propagator.step()

        self.assertFalse(self.two_in_contact[0].infected)
        self.assertFalse(self.two_in_contact[1].infected)

    def test_propagator_step_one_infected_unity_rate_infects_other(self):
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=1.0)

        propagator.step()

        self.assertTrue(self.two_in_contact[1].infected)

    @mock.patch('random.random')
    def test_propagator_step_half_rate_infects_other_with_rng_zero(self, mock_random):
        mock_random.return_value = 0.0
        self.two_in_contact[0].infected = True
        propagator = Propagator(self.two_in_contact, rate=0.5)

        propagator.step()

        self.assertTrue(self.two_in_contact[1].infected)
