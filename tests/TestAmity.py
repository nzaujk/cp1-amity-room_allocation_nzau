""" Unit tests for the methods in the
Amity Class"""
import os
import unittest
from modules.amity import Amity
from modules.room import LivingSpace,Office


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.test_amity = Amity()

    def test_create_living_space(self):
        """
        This is testing for when a user creates living spaces
        """
        self.test_amity.create_room('living space',['Braavos'])
        self.assertEqual(len(self.test_amity.room_directory),1, "Braavos has been successfully created!")

    def test_create_office(self):
        """
        This is testing for when a user creates offices
        """
        self.test_amity.create_room('office',['Valyria'])
        self.assertEqual(len(self.test_amity.room_directory), 1, "Valyria has been successfully created!")

    def test_room_does_not_exist(self):
        office_space = self.test_amity.create_room("office", ["Old Town"])
        self.assertEqual(office_space, "room exists")

    def test_add_person_fellow(self):
        self.test_amity.add_person("Joe", "Nzau", "FELLOW", "Y")
        self.assertNotEqual(len(self.test_amity.unallocated_living_space), 1)

    def test_add_person_staff(self):
        self.test_amity.add_person("Pauline", "Magda", "STAFF")
        self.assertNotEqual(len(self.test_amity.unallocated_office), 1)

    def test_random_generating_office_room(self):
        self.test_amity.create_room('office', ["WinterFell"])
        self.test_amity.create_room('office', ['Westeros'])
        random_office = self.test_amity.generating_random_office()
        self.assertIn(random_office, self.test_amity.office)

    def test_random_generating_living_space(self):
        self.test_amity.create_room("living space", ["King's Landing"])
        self.test_amity.create_room('living space', ['Casterly Rock'])
        random_living_space = self.test_amity.generating_random_living_space()
        self.assertIn(random_living_space, self.test_amity.living_space)

    def test_file_path(self):
        self.test_amity.load_people(filename="amity_load.txt")
        self.assertTrue(os.path.exists("amity_load.txt"))
        os.remove("amity_load.txt")

    def test_print_allocations(self):
        file = open(os.path.join("amity_load.txt"))
        lines = file.readlines()
        self.assertTrue("Casterly Rock\n" in lines)
        self.assertTrue("WinterFell\n" in lines)
        os.remove("amity_load.txt")

    def test_print_unallocated(self):
        self.test_amity.print_unallocated_people('file')
        self.assertTrue(os.path.isfile('amity_load.txt'))
        os.remove('amity_load.txt')

    def test_print_rooms(self):
        self.test_amity.print_rooms_and_allocated_members('file')
        self.assertTrue(os.path.isfile('amity_load.txt'))
        os.remove('amity_load.txt')

    def test_saves_state(self):
        Amity.save_state('amity_db')
        self.assertTrue(os.path.isfile('amity_db.sqlite'))


if __name__ == '__main__':
    unittest.main()


