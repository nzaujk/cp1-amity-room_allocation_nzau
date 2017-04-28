
import os
import unittest
import sys
from io import StringIO
from contextlib import contextmanager
from modules.amity import Amity
from modules.person import *
from modules.room import Room,Office,LivingSpace


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.test_amity = Amity()
        self.test_person = Person
        self.test_room = Room

    @contextmanager
    def captured_output(self): # pragma: no cover

        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_is_fellow(self):
        """test that that fellow is an instance of Person class"""
        is_fellow = Person("Joe", "Irungu", "fellow")
        self.assertEqual(is_fellow.role, "fellow")

    def test_is_staff(self):
        """test that staff is an instance of Person class"""
        is_staff = Person("Jack", "Kamau", "staff")
        self.assertEqual(is_staff.role, "staff")

    def test_office(self):
        """test that office takes 6 spaces"""
        self.test_office = Office("Bravos")
        self.assertEqual(self.test_office.capacity, 6)

    def test_living_space(self):
        """test that living space takes space of 4 """
        self.test_living_space = LivingSpace("Volantis")
        self.assertEqual(self.test_living_space.capacity, 4)

    def test_create_living_space(self):
        """
        This is testing for when a user creates living spaces
        """

        self.assertEqual(self.test_amity.create_room("living_space", ["Itajuba"]),
                         "operation successful")

    def test_create_office(self):
        """
        This is testing for when a user creates offices
        """

        self.assertEqual(self.test_amity.create_room("office", ["Valyris"]),"operation successful")

    def test_room_name_already_exists(self):
        """check if the new room name already exists"""
        self.test_amity.create_room("office", ["Westeros", "Pintos"])
        self.assertEqual("operation not successful",self.test_amity.create_room("office", ["Westeros", "Pintos"]))

    def test_add_person_fellow_and_allocate_ls_and_office(self):
        """add person function will also allocate space to staff and fellow"""
        self.test_amity.create_room("office", ["Meskel Square"])
        self.test_amity.create_room("living_space", ["Torailhoch"])
        self.assertEqual(self.test_amity.add_person("Wangeci", "Mbogo", "fellow", "y"),
                         "operation successful")

    def test_add_person_staff_and_allocate_office(self):
        self.create_office = self.test_amity.create_room("office", ["Valyris"])
        self.assertEqual(self.test_amity.add_person("Pauline", "Magda", "staff"),
                         "operation successful")

    def test_staff_cannot_be_allocated_living_space(self):
        self.test_amity.create_room("office", ["Pinto"])
        self.assertEqual(self.test_amity.add_person("Joe", "Ouma", "staff","y"),
                                          "Office allocation successful."
                                          " Living space allocation not successful")

    def test_person_is_not_duplicate(self):
        """Test that names are not duplicated when added"""
        self.test_amity.add_person("Mercy", "Ogutu", "staff")
        self.assertEqual(self.test_amity.add_person("Mercy", "Ogutu","fellow"),
                         'operation not successful')

    def test_random_generating_office_room(self):
        self.test_amity.create_room('office', ["WinterFell"])
        self.test_amity.create_room('office', ['Westeros'])
        random_office = self.test_amity.generating_random_office()
        self.assertIn(random_office, self.test_amity.office)

    def test_random_generating_living_space(self):

        self.test_amity.create_room('living_space', ["Namibia"])
        self.test_amity.create_room('living_space', ['Kaldys'])
        random_living_space = self.test_amity.generating_random_living_space()
        self.assertIn(random_living_space, self.test_amity.living_space)

    def test_it_does_not_reallocate_to_a_full_office(self):
        """Populate the rooms and add a 7 th person test if reallocate does not
        realllocate to a full room"""
        self.test_amity.create_room("office",["Stone Town"])
        self.test_amity.add_person("Mike","Mwaniki","staff")
        self.test_amity.add_person("Lilian","Wanjiru","staff")
        self.test_amity.add_person("Yvonne", "Makena", "fellow")
        self.test_amity.add_person("Mwikali", "Mwende", "fellow")
        self.test_amity.add_person("Mustafa","Ahmed","staff")
        self.test_amity.add_person("Moses","Makeni","fellow")
        self.test_amity.add_person("Miriam", "Salome ", "staff")
        """reallocating new member after poplating the office"""
        self.assertEqual(self.test_amity.reallocate_person_to_office("Miriam","Salome ","Stone Town"),
                         "operation not successful.room is full")

    def test_it_does_not_reallocate_to_a_full_living_space(self):
        self.test_amity.create_room("living_space",["Nungwi"])
        self.test_amity.add_person("Mike","Mwaniki","fellow","y")
        self.test_amity.add_person("Lilian","Wanjiru","fellow", "y")
        self.test_amity.add_person("Yvonne", "Makena", "fellow", "y")
        self.test_amity.add_person("Mwikali", "Mwende", "fellow","y")

        self.assertEqual(self.test_amity.reallocate_person_to_living_space("Mwikali","Mwende","Nungwi"),
                         "operation not successful.room is full")

    def test_it_does_not_reallocate_to_none_existing_office(self):
        self.test_amity.add_person("Winnie", "Chebet", "fellow", "y")

        self.assertEqual(self.test_amity.reallocate_person_to_office("Winne","Chebet","NewCabin"),
                         "operation not successful.room does not exist")

    def test_it_does_not_reallocate_to_none_existing_living_space(self):
        self.test_amity.add_person("Winnie", "Chebet", "fellow", "y")

        self.assertEqual(self.test_amity.reallocate_person_to_living_space("William","Chebet","NewTown"),
                         "operation not successful.room does not exist")

    def test_it_does_not_reallocate_to_the_same_office(self):
        self.test_amity.create_room("office", ["Shire"])
        self.test_amity.add_person("Maina", "Chege", "staff")
        self.assertEqual(self.test_amity.reallocate_person_to_office("Maina", "Chege", "Shire"),
                         "operation not successful.reallocating to same place")

    def test_it_does_not_reallocate_to_the_same_living_space(self):
        self.test_amity.create_room("living_space", ["Shire"])
        self.test_amity.add_person("Maina", "Chege", "fellow","y")
        self.assertEqual(self.test_amity.reallocate_person_to_living_space("Maina","Chege","Shire"),
                         "operation not successful.reallocating to same place")

    def test_it_reallocates_to_office_successfully(self):
        """Test that the reallocation is successful"""
        self.test_amity.add_person("Beza", "Shewarega","staff")
        self.test_amity.create_room("office", ["Ledeta"])
        self.assertEqual(self.test_amity.reallocate_person_to_office("Beza","Shewarega","Ledeta"),
                         "operation successful")

    def test_it_reallocates_to_living_space_successfully(self):
        self.test_amity.add_person("Fewa", "Salamna","fellow","y")
        self.test_amity.create_room("living_space", ["Piassa"])
        self.assertEqual(self.test_amity.reallocate_person_to_living_space("Fewa","Salamna","Piassa"),
                         "operation successful")

    def test_fellow_added_to_unallocated_space_if_no_office_available(self):
        self.test_amity.create_room("living_space", ["OldValyris"])
        self.assertEqual(self.test_amity.add_person("Miriam","Wangui", "fellow", "y"),
                         "operation successful but added to unallocated list")

    def test_fellow_added_to_unallocated_space_if_no_living_available(self):
        self.test_amity.create_room("office", ["Mariabi"])
        self.assertEqual(self.test_amity.add_person("Olivia", "Ferel", "fellow", "y"),
                         "operation successful but added to unallocated list")

    def test_fellow_added_to_unallocated_space_if_both_no_living_available_or_office_available(self):
        self.assertEqual(self.test_amity.add_person("Olivia", "Ferel", "fellow", "y"),
                         "Operation not successful.Added to unallocated")

    def test_fellow_added_to_unallocated_space_if_they_choose_n(self):
        self.assertEqual(self.test_amity.add_person("Olivia", "Ferel", "fellow", "n"),
                         "operation successful:unallocated list")

    def test_fellow_added_to_unallocated_space_if_they_choose_n_and_no_office_available(self):
        self.test_amity.create_room("office", ["OldCity"])
        self.assertEqual(self.test_amity.add_person("Olivia", "Ferel", "fellow", "n"),
                         "operation successful")

    def test_staff_added_to_unallocated_space_if_no_office_available(self):
        """if staff is added but no office is available they should be added to a list
        of unallocated offices"""
        self.assertEqual(self.test_amity.add_person("Miriam","Wangui", "staff"),
                         "Office not successful.Added to unallocated list")

    def test_staff_added_to_unallocated_space_if_no_office_available(self):
        """check if staff is still added to unallocated space for office
        if they choose living space"""
        self.assertEqual(self.test_amity.add_person("Mary", "Wangui", "staff", "y"),
                         "Added to unallocated list. Living space allocation not successful")

    def test_add_person_not_a_valid_role(self):
        """test that function does not accept other roles except staff and fellow"""
        self.assertEqual(self.test_amity.add_person("Wambui","Kamau","client"), "not a valid role")

    def test_staff_is_deleted_from_office(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.create_room("office", ["Piassa"])
        self.test_amity.add_person("Monica", "Winnie", "staff")
        remove_person = self.test_amity.delete_employee("Monica","Winnie")
        self.assertEqual(remove_person, "staff deleted")

    # def test_fellow_is_deleted_from_living_space(self):
    #     """test that person is no longer existing after the remove function is called"""
    #     self.test_amity.create_room("living_space",["Menelik"])
    #     self.test_amity.create_room("office", ["Meganagha"])

        # self.test_amity.add_person("Bonny", "Khaemba", "fellow", "y")
        # remove_person = self.test_amity.delete_employee("Bonny", "Khaemba",)
        # self.assertEqual(remove_person, "fellow deleted")

    def test_staff_is_deleted_from_unallocated_office_space(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.add_person("Wendy", "Maina", "staff")
        remove_person = self.test_amity.delete_employee("Wendy", "Maina")
        self.assertEqual(remove_person, 'staff deleted')

    def test_fellow_is_deleted_from_unallocated_living_space_and_unallocated_office(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.add_person("Mbaire", "Elizabeth", "fellow", "y")
        remove_person = self.test_amity.delete_employee("Mbaire","Elizabeth")
        self.assertEqual(remove_person, 'deleted from unallocated space')

    def test_fellow_is_deleted_from_unallocated_office_and_living_space(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.create_room("living_space", ["BoleAtlas"])
        self.test_amity.add_person("Sylvia", "Leah", "fellow", "y")
        remove = self.test_amity.delete_employee("Sylvia", "Leah")
        self.assertEqual(remove, "deleted from unallocated space")

    def test_fellow_is_deleted_from_office_and_unallocated_living_space(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.create_room("office", ["AtikilTera"])
        self.test_amity.add_person("Alex", "Ouma", "fellow", "y")
        remove = self.test_amity.delete_employee("Alex", "Ouma")
        self.assertEqual(remove, "fellow deleted")

    def test_delete_employee_cannot_delete_person_not_in_system(self):
        """test system cannot delete None"""
        remove_person = self.test_amity.delete_employee("Wambui", "Murithi")
        self.assertEqual(remove_person, 'operation not successful.person does not exist')

    def test_fellow_is_deleted_from_office_and_living_space(self):
        """test that person is no longer existing after the remove function is called"""
        self.test_amity.create_room("office", ["MesekelSquare"])
        self.test_amity.create_room("living_space", ["BoleBrass"])
        self.test_amity.add_person("Kevin", "Maina", "fellow", "y")
        remove_person = self.test_amity.delete_employee("Kevin","Maina")
        self.assertEqual(remove_person, "fellow deleted")

    def test_it_prints_unallocated(self):
        self.test_amity.print_unallocated('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_print_allocations(self):
        self.test_amity.print_allocations('file')
        self.assertTrue(os.path.isfile('file.txt'))
        os.remove('file.txt')

    def test_print_rooms_doesnt_exist(self):
        self.test_amity.create_room("living_space", ["Lobu"])
        self.assertEqual(self.test_amity.print_rooms('GojamBerenda'),
                         "room does not exist")

    def test_print_rooms_living_space(self):
        """test if the function prints the people in a given living space"""
        self.test_amity.create_room("living_space", ["OldAirport"])
        self.test_amity.add_person("Moses", "Kioko","fellow", "y")
        self.assertEqual(self.test_amity.print_rooms("OldAirport"),"person in room")

    def test_print_rooms_office(self):
        """test if the function prints the people in a given office"""
        self.test_amity.create_room("office", ["OldAirport"])
        self.test_amity.add_person("Moses", "Kioko","fellow")
        self.assertEqual(self.test_amity.print_rooms("OldAirport"),"person in room")

    def test_print_rooms_invalid_name(self):
        """test if the function returns ans exception when user mispels the name
        of a room"""
        self.test_amity.create_room("office", ["OldAirport"])
        self.test_amity.add_person("Moses", "Kioko","fellow")
        self.assertEqual(self.test_amity.print_rooms("OldAIrport"),"Invalid")

    def test_saves_state_to_db(self):
        self.test_amity.create_room("office", ["Mexico"])
        self.test_amity.save_state('amity_db')
        self.assertTrue(os.path.isfile('amity_db.sqlite'))
        os.remove("amity_db.sqlite")

    def test_saves_state(self):
        self.test_amity.create_room("office", ["StGabriels"])
        self.test_amity.add_person("Tina", "Murimi","staff")
        self.assertEqual(self.test_amity.save_state('amity_db'), "saved status")

    def test_load_state_to_db(self):
        self.test_amity.create_room("office", ["Mexico"])
        self.test_amity.save_state('amity_db')
        self.test_amity.load_state('amity_db')
        self.assertTrue(os.path.isfile('amity_db.sqlite'))
        os.remove("amity_db.sqlite")

    def test_load_state_to_db(self):
        self.test_amity.create_room("office", ["Mexico"])
        self.assertEqual(self.test_amity.load_state("amity_db"), "operation successful")

if __name__ == '__main__':
    unittest.main() # pragma: no cover

