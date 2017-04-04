import unittest
import os
from modules.amity import Amity, Room
from modules.person import Person, Fellow, Staff
from modules.room import Office, LivingSpace


class TestClassInheritance(unittest.TestCase):
    def setUp(self):
        self. test_amity = Amity
        self.test_person = Person
        self.fellow = Fellow
        self.staff = Staff
        self.living_space = LivingSpace
        self.office = Office

    '''checks the class relationships'''

    def test_office_is_subclass(self):
        self.assertIsInstance(Office, Room)

    def test_living_space_is_subclass(self):
        self.assertIsInstance(LivingSpace, Room)

    def test_room_is_subclass(self):
        self.assertIsInstance(Room, Amity)

    def test_staff_is_subclass(self):
        self.assertIsInstance(Staff, Person)

    def test_fellow_is_subclass(self):
        self.assertIsInstance(Fellow, Person)

    def test_create_living_space(self):
        '''test if it creates living space and assert has 4 spaces'''
        self.assertEqual(self.living_space.create_room, 4)

    def test_create_office(self):
        '''test if it creates office  and has 6 spaces'''
        self.assertEqual(self.office.create_room, ["room name"])

    def test_room_is_office(self):
        '''test if room created is an office'''
        self.assertEqual(self.test_amity.create_room, {"Valarys":"Office"})

    def test_room_is_living_space(self):
        '''test if room created is a living space'''
        self.assertEqual(self.test_amity.create_room, {"King's Landing":"Living Space"})

    def test_room_exists(self):
        '''test if a room exists from a list of rooms'''
        self.assertIn(self.test_amity.view_rooms, ["King's Landing"])

    def test_check_office_has_space(self):
        '''test if office has space. If list is equal to 6 the office space is full.'''
        self.assertEqual(self.office.check_office_has_space, 6)

    def test_check_living_space_has_space(self):
        '''test if the living space has space. If the allocated is 4 it raises an assert'''
        self.assertEqual(self.living_space.check_living_space_has_space, 4)

    def test_add_person(self):
        '''tests that person has been created'''
        self.add_person = Person()
        self.new_person = self.staff or self.fellow
        self.assertEqual(self.new_person.add_person, {"emp_id": "name"} )

    def test_add_staff(self):
        '''Test adding of new staff'''
        self.new_staff = self.staff
        self.assertEqual(self.new_staff.add_staff, {"emp_id": "name"})

    def test_add_fellow(self):
        '''Test adding of new fellow'''
        self.new_fellow = Fellow
        self.assertEqual(self.new_fellow.add_fellow, {"emp_id": "name"})

    def test_is_fellow(self):
        '''Test that person is a fellow'''
        self.a_person = Fellow()
        self.assertTrue(self.a_person.is_fellow, msg= "Person is a fellow" )

    def test_is_staff(self):
        '''Check name doesnt exist'''
        self.a_person = Staff
        self.assertTrue(self.a_person.is_staff, )

    def test_name_exists(self):
        ''' test if name for room create exists '''
        self.assertEqual(self.test_amity.view_rooms, "Name exists")

    def test_check_duplicate_person_to_office(self):
        '''test if person is already allocated.'''
        self.allocate_person = Person()
        self.assertEqual(self.allocate_person.view_allocated,"Person already exists")

    def test_allocate_person(self):
        self.test_allocate = Person()
        self.allocate_person = {"Person": ["id"], Staff:True, Fellow:True}
        self.assertTrue(self.allocate_person, True)

    def test_load_people(self):
        '''Test that people can be added to the app from a text'''
        self.test_load = Room
        self.assertEqual(self.test_load.load_people, "amity_load.txt")


if __name__ == '__main__':
    unittest.main()
