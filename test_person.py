from unittest import TestCase

from person import Person


class TestPerson(TestCase):
    person: Person

    def setUp(self) -> None:
        self.person = Person()

    def test_has_empty_contact_array(self):
        self.assertEqual([], self.person.contacts)

    def test_starts_not_infected(self):
        self.assertFalse(self.person.infected)

    def test_starts_not_dead(self):
        self.assertFalse(self.person.dead)

