""" Unit tests for the methods in the
Amity Class"""
import os
import sys
import unittest
from modules.amity import Amity
from modules.person import *
from modules.room import Room,Office,LivingSpace


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.test_amity = Amity()
        self.test_person = Person
        self.test_room = Room

    def test_is_fellow(self):
        is_fellow = Person("Joe", "Irungu", "FELLOW")
        self.assertEqual(is_fellow.role, "FELLOW")

    def test_is_staff(self):
        is_staff = Person("Jack", "Kamau", "STAFF")
        self.assertEqual(is_staff.role, "STAFF")

    def test_office(self):
        self.test_office = Office("Bravos")
        self.assertEqual(self.test_office.capacity, 6)

    def test_living_space(self):
        self.test_living_space = LivingSpace("Volantis")
        self.assertEqual(self.test_living_space.capacity, 4)

    def test_create_living_space(self):
        """
        This is testing for when a user creates living spaces
        """
        self.test_amity.create_room('living_space',['Braavos'])
        self.assertEqual(len(self.test_amity.room_directory),1, "Braavos has been successfully created!")

    def test_create_office(self):
        """
        This is testing for when a user creates offices
        """
        self.test_amity.create_room('office',['Valyria'])
        self.assertEqual(len(self.test_amity.room_directory), 1, "Valyria has been successfully created!")

    def test_room_name_exists(self):
        """check if the new room name already exists"""
        self.assertEqual(len(self.test_amity.room_directory), 0)
        self.total_rooms = len(self.test_amity.room_directory)
        self.test_amity.create_room('living room', ['Old Town'])
        self.test_amity.create_room('office', ['Old Town'])
        self.test_amity.create_room('living room', ['Old Town'])
        self.assertEqual(len(self.test_amity.room_directory), 1,
                         'Rooms cannot have duplicate names!')

    def test_add_person_fellow(self):
        self.test_amity.add_person("Joe", "Nzau", "FELLOW", "Y")
        self.assertEqual(len(self.test_amity.fellow), 1, "Added: {0} and allocated them to {0}")\


    def test_person_is_not_duplicate(self):
        self.test_amity.check_add_person_duplicate("Mike","Mbuvi")
        self.assertEqual(len(self.test_amity.employees), 0, '{0} is already in the system.')

    def test_add_person_staff(self):
        self.test_amity.add_person("Pauline", "Magda", "STAFF")
        self.assertEqual(len(self.test_amity.staff), 1, "Added: {0} and allocated them to {0}")

    def test_add_unallocated_living_space(self):
        self.test_amity.add_person("Kevin", "Tuju", "FELLOW", "Y")
        self.assertEqual(len(self.test_amity.unallocated_living_space), 1, "Added Kevin Tuju to the unallocated list")

    def test_add_unallocated_office(self):
        self.test_amity.add_person("Mercy", "Mwongeli", "STAFF",)
        self.assertEqual(len(self.test_amity.unallocated_office), 1, "Added Mercy Mwongeli to the unallocated list")

    def test_random_generating_office_room(self):
        self.test_amity.create_room('office', ["WinterFell"])
        self.test_amity.create_room('office', ['Westeros'])
        random_office = self.test_amity.generating_random_office()
        self.assertIn(random_office, self.test_amity.office)

    def test_random_generating_living_space(self):
        self.test_amity.create_room('living_space', ["Reebook"])
        self.test_amity.create_room('living_space', ["TheNorth"])
        random_living_space = self.test_amity.generating_random_living_space()
        self.assertIn(random_living_space, self.test_amity.living_space)

    def test_reallocation_to_office(self):
        self.test_amity.create_room('office', ['Volantis'])
        self.test_amity.add_person('Steve', 'Kwamboka', 'FELLOW', 'Y')
        self.assertIn('Steve Kwamboka', self.test_amity.office['Volantis'])
        self.test_amity.create_room('office', ['Netherealmn'])
        self.test_amity.reallocate_person_to_office('Steve Kwamboka','Netherealmn')
        self.assertIn('Steve Kwamboka', self.test_amity.office['Netherealmn'])
        self.assertNotIn('Steve Kwamboka', self.test_amity.office['Volantis'])

    def test_reallocation_to_living_space(self):
        self.test_amity.create_room('living_space', ['Shire'])
        self.test_amity.add_person('Mercy', 'Flavia', 'FELLOW', 'Y')
        self.assertIn('Mercy Flavia', self.test_amity.living_space['Shire'])
        self.test_amity.create_room('living_space', ['Modor'])
        self.test_amity.reallocate_person_to_living_space('Mercy Flavia','Modor')
        self.assertIn('Mercy Flavia', self.test_amity.living_space['Modor'])
        self.assertNotIn('Mercy Flavia', self.test_amity.living_space['Shire'])

    def test_it_does_not_reallocate_none_existent_room(self):
        self.test_amity.create_room('office', ['Ubuntu'])
        self.test_amity.add_person('Miriam', 'Cate', 'Fellow')
        response = self.test_amity.reallocate_person_to_office('office', ['Ubuntu'])
        self.assertEqual(response, "Miriam Cate is already allocated to Ubuntu")

    def test_file_path(self):
        self.test_amity.load_people(filename="amity_load")
        self.assertTrue(os.path.exists("amity_load.txt"))
        os.remove("amity_load")

    def test_print_unallocated(self):
        self.test_amity.print_unallocated('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_print_allocations(self):
        self.test_amity.print_allocations('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_print_rooms(self):
        self.test_amity.print_rooms('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_saves_state(self):
        self.test_amity.save_state('amity_db')
        self.assertTrue(os.path.isfile('amity_db.sqlite'))


if __name__ == '__main__':
    unittest.main()


