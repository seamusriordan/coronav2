from unittest import TestCase

from person import Person


class TestPerson(TestCase):

    def testHasEmptyContactArray(self):
        person = Person()
        self.assertEqual([], person.contacts)
