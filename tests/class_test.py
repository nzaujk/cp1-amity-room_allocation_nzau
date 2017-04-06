import unittest
from modules.amity import Amity, Room
from modules.person import Person, Fellow, Staff
from modules.room import Office, LivingSpace


class TestClassInheritance(unittest.TestCase):
    def setUp(self):
        self.test_amity = Amity()
        self.test_person = Person()
        self.fellow = Fellow()
        self.staff = Staff()
        self.living_space = LivingSpace()
        self.office = Office()


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
        '''test if it creates living space'''
        self.assertEqual(self.test_amity.create_room,
                         ({"room_name": "Westeros",
                                 "office": False,
                                 "living_space": True}))

    def test_create_office(self):
        '''test if it creates office  and has 6 spaces'''
        self.assertEqual(self.test_amity.create_room, (self.test_amity.create_room,
                         ({"room_name": "King's Landing",
                                 "office": True,
                                 "living_space": False})))

    def test_room_exists(self):
        '''test if a room exists from a list of rooms'''
        self.test_amity.new_room = {self.office: "King's Landing"}
        self.assertEqual(self.test_amity.view_rooms,({"room name": "King's Landing"}))

    def test_available_office(self):
        '''test if office has space. If list is equal to 6 the office space is full.'''
        self.assertEqual(self.office.check_office_has_space, {"capacity": 6})

    def test_available_living_space(self):
        '''test if the living space has space. If the allocated is 4 it raises an assert'''
        self.assertEqual(self.living_space.check_living_space_has_space, {"capacity": 4})

    def test_add_fellow(self):
        '''tests that fellow has been created'''
        self.assertEqual(self.fellow.add_fellow, {"23456": "Joe Nzau"})

    def test_add_staff(self):
        '''Test adding of new staff'''
        self.assertEqual(self.fellow.add_fellow, {"4567": "Joey Mungai"})

    def test_is_fellow(self):
        '''Test that person is a fellow'''
        self.assertEqual(self.fellow.is_fellow, {"emp_id":"name", self.staff: False, self.fellow: True})

    def test_is_staff(self):
        '''Check name doesnt exist'''
        self.assertEqual(self.staff.is_staff, {"emp_id": "name", self.staff: True, self.fellow: False})

    def test_name_exists(self):
        ''' test if name for room create exists '''
        self.assertEqual(self.test_amity.view_rooms, {"room_name":"room_type"})

    def test_check_duplicate_person_to_office(self):
        '''test if person is already allocated.'''
        self.allocate_person = Person()
        self.assertEqual(self.allocate_person.view_allocated, {"emp_id": "name"})

    def test_allocate_office(self):
        '''allocate office to person'''
        self.assertEqual(self.test_amity.allocate_person, {"emp_id": 'name', Staff: True, Fellow:True} )

    def test_allocate_living_space(self):
        '''allocate living space to person'''
        self.assertEqual(self.test_amity.allocate_person, {'emp_id': 'name', Staff: False, Fellow: True})

    def test_load_people(self):
        '''Test that people can be added to the app from a text'''
        self.test_load = Room
        self.assertEqual(self.test_load.load_people, "amity_load.txt")


if __name__ == '__main__':
    unittest.main()
