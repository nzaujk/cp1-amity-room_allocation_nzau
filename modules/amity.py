"""Amity class which contains the subclasses and methods
to create rooms,add people and allocate/reallocate rooms"""
import os
import random
from modules.room import LivingSpace,Office
from modules.person import Fellow, Staff


class Amity (object):
    def __init__(self):
        self.room_directory = []
        self.vacant_office = []
        self.vacant_living_space = []
        self.full_room_directory = []
        self.unallocated_office = {}
        self.unallocated_living_space = {}
        self.staff = []
        self.fellow = []
        self.living_space = {"None": []}
        self.office = {"None": []}
        self.employees = {}

    def create_room(self, room_type, room_name):
        """Check room does not exist."""
        for room in room_name:
            if room in [room.room_name for room in self.room_directory]:
                print('Sorry, room name already exists.')

            if room_type == 'office':
                new_office = Office(room)
                self.room_directory.append(new_office)
                self.vacant_office.append(new_office)
                print("{0} has been successfully created!".format(new_office.room_name))

            elif room_type == 'living space':
                new_living_space = LivingSpace(room)
                self.room_directory.append(new_living_space)
                self.vacant_living_space.append(new_living_space)
                print('{0} has been successfully created!'.format(new_living_space.room_name))

    def generating_random_office(self):
        """generates random offices to be allocated by the add person function"""
        self.vacant_office = [space for space in self.office if len(self.office[space]) < 6]

        if len(self.vacant_office) >= 0:
            random_office = random.choice(self.vacant_office)
            return random_office
        else:
            print("No office available.Please try later")

    def generating_random_living_space(self):
        """generates random living spaces to be allocated by the add person function"""
        self.vacant_living_space = [space for space in self.living_space if len(self.living_space[space]) < 4]

        if len(self.vacant_living_space) >= 0:
            random_living_space = random.choice(self.vacant_living_space)
            return random_living_space
        else:
            print('No living space available.Please try later')

    def add_person(self,first_name, last_name, role, wants_accommodation='N'):
        """Adds a person into the system"""
        emp_name = first_name + " " + last_name

        if emp_name.title() in self.employees:
            print('Person with {0} id already exist.' .format(emp_name))

        elif role.upper() == 'FELLOW' and wants_accommodation.upper() == 'Y':
            new_fellow = Fellow(first_name, last_name)
            """adding employee to the fellows list"""
            self.employees[new_fellow.name.title()] = role
            self.fellow.append(new_fellow.name.title())
            """randomly allocate office and living space """
            random_office = Amity.generating_random_office(self)
            random_living_space = Amity.generating_random_living_space(self)

            if not random_office and not random_living_space:
                """If person is not given an office or a living space"""
                self.unallocated_office[new_fellow.name.title()] = role
                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {0} to the unallocated list'.format(new_fellow.name))

            elif not random_office and random_living_space:
                """if person is not being allocated a random office  but
                will be allocated a random living space"""

                self.unallocated_office[new_fellow.name.title()] = role
                print('Added {0} to the unallocated list' .format(new_fellow.name))
                self.living_space[random_living_space].append(new_fellow.name.title())
                print("Added: {0} and allocated them to a living space "
                      "{0}: ".format(new_fellow.name, random_living_space))
            elif not random_living_space and random_office:
                """If person is not being allocated a living space but will be allocated
                an office"""

                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {0} to the unallocated list' .format(new_fellow.name))
                self.office[random_office].append(new_fellow.name.title())
                print("Added: {0} and allocated them to an office {0}: "
                      .format(new_fellow.name, random_office))

            else:
                """allocate person both office and living space"""
                self.office[random_office].append(new_fellow.name.title())
                print("Added: {0} and allocated them to {0}: " .format(new_fellow.name, random_office))
                self.living_space[random_living_space].append(new_fellow.name.title())
                print("Added: {0} and allocated them to {0}: " .format(new_fellow.name, random_living_space))

        elif role.upper() == 'FELLOW':
            """if person is a fellow but selects no to receive living space
            the default is No"""
            new_fellow = Fellow(first_name, last_name)
            self.employees[new_fellow.name.title()] = role
            self.fellow.append(new_fellow.name.title())
            random_office = Amity.generating_random_office()
            if not random_office:
                self.unallocated_office[new_fellow.name.title()] = role
                print('Added{0} to the unallocated list' .format(new_fellow.name))
            else:
                self.office[random_office].append(new_fellow.name.title())
                print("Added: {0} and allocated them to {0}: ".format(new_fellow.name, random_office))

        elif role.upper() == 'STAFF' and wants_accommodation.upper() == 'Y':
            """adds person to the staff list"""
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name.title()] = role
            self.staff.append(new_staff.name)
            random_office = Amity.generating_random_office()
            if not random_office:
                self.unallocated_office[new_staff.name.title()] = role
                print('Added %s to the unallocated list' % new_staff.name)
                print('Staff cannot be allocated a living space')
            else:
                self.office[random_office].append(new_staff.name.title())
                print("Added: {0} and allocated them to {0}: " % (new_staff.name, random_office))
                print('Staff cannot be allocated a living space')

        elif role.upper() == 'STAFF':
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name.title()] = role
            self.staff.append(new_staff.name.title())
            random_office = Amity.generating_random_office(self)
            if not random_office:
                """allocate a random office to staff"""
                self.unallocated_office[new_staff.name.title()] = role
                print('Added {0} to the unallocated list' .format(new_staff.name))
            else:
                self.office[random_office].append(new_staff.name.title())
                print("Added: {0} and allocated them to {0}: " .format(new_staff.name, random_office))

        else:
            print('{0} is not a valid role.' .format(role))

    def reallocate_person(self, first_name, last_name, room_type, new_room):
        full_name = first_name.title() + " " + last_name.title()
        """Check if the person is a member"""
        self.fellow = [fellow.name for fellow in self.employees if fellow.role == "FELLOW"]
        self.staff = [staff.name for staff in self.employee if staff.role == "STAFF"]
        self.vacant_living_space = [room.name for room in self.living_space if room.room_type == "living space"
                              and len(self.living_space[room.name]) < 4]
        self.vacant_office = [room.name for room in self.living_space if room.rom_type == "office"
                      and len(self.office[room.name]) < 6]
        if full_name not in self.fellow and full_name not in self.staff:
            print("The person doesn't exist.")
        elif new_room.title() not in self.vacant_living_space and new_room.title() not in self.vacant_office:
            print("The room requested does not exist or is not available please choose a different room")

        else:
            if room_type == "living space":
                """if a room that exists is an office but not a living space"""
                if new_room not in self.vacant_living_space:
                    print("The room selected is not a LivingSpace.")
                elif full_name not in self.fellow:
                    print("Only fellows can get a room")
                else:
                    for room in self.living_space.keys():
                        if full_name in self.living_space[room]:
                            changing_location = self.living_space[room]
                            changing_location.remove(full_name)
                            self.office[new_room.title()].append(full_name)
                            print("{0} successfuly reallocated to {0}".format(full_name, new_room))
            elif room_type == "office":
                if new_room not in self.vacant_office:
                    print("The room selected is not an office")
                else:
                    for room in self.office.keys():
                        if full_name in self.office[room]:
                            changing_location = self.office[room]
                            changing_location.remove(full_name)
                            self.office[new_room.title].append(full_name)
                            print("{0} successfuly reallocated to {0}" .format(full_name, new_room))

    def load_people(self, filename):
        """Loads people to the system from a text file."""
        if os.path.isfile(filename + ".txt"):
            file = open(filename + ".txt").readlines()
            for line in file:
                person_data = line.split()
                if len(person_data) == 4:
                    Amity.add_person(first_name=person_data[0], last_name=person_data[1],
                                     role=person_data[2], wants_accommodation=person_data[3])
                elif len(person_data) == 3:
                    Amity.add_person(first_name=person_data[0], last_name=person_data[1],
                                    role=person_data[2], wants_accommodation='N')
                else:
                    print('the file format is not valid')
        else:
            print('cannot access the file')

    def print_allocation_spaces(self,filename):
        pass

    def print_unallocated_people(self, filename):
        pass

    def print_rooms_and_allocated_members(self, filename):
        pass

    def save_state(self, filename):
        pass
