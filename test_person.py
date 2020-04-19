from unittest import TestCase

from person import Person


class TestPerson(TestCase):

    def test_has_empty_contact_array(self):
        person = Person()
        self.assertEqual([], person.contacts)

    def test_starts_not_infected(self):
        person = Person()
        self.assertFalse(person.infected)
