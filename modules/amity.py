"""Amity class which contains the subclasses and methods
to create rooms,add people and allocate/reallocate rooms"""

import random
from sqlalchemy.sql import select
from collections import defaultdict
from modules.room import LivingSpace,Office
from modules.person import Fellow, Staff
from db.amity_db import Base, AmityDatabaseLoad,PersonDB,RoomDB,OfficeDB,\
    LivingSpaceDB, UnallocatedDB


class Amity (object):

    def __init__(self):
        self.room_directory = {}
        self.vacant_office = []
        self.vacant_living_space = []
        self.unallocated_office = {}
        self.unallocated_living_space = {}
        self.staff = []
        self.fellow = []
        self.employees = {}
        self.living_space = defaultdict(list)
        self.office = defaultdict(list)

    def create_room(self, room_type, room_name):
        """Check room does not exist."""
        for room in room_name:
            if room in self.room_directory:
                print("{} Exists".format(room))

            if room_type == 'office':
                new_office = Office(room)
                """adding key value pair"""
                self.room_directory[new_office.room_name.title()] = new_office.room_type
                self.office[new_office.room_name.title()] = room_type
                print("{}: {} has been successfully created!".format(room_type,new_office.room_name))

            elif room_type == 'living_space':
                new_living_space = LivingSpace(room)
                self.room_directory[new_living_space.room_name.title()] = new_living_space.room_type
                self.living_space[new_living_space.room_name.title()] = room_type
                print("{}: {} has been successfully created!".format(room_type, new_living_space.room_name))

    def check_add_person_duplicate(self,first_name, last_name):
        """Adds a person into the system"""
        full_name = first_name + " " + last_name

        if full_name.title() in self.employees:
            print('{} is already in the system.'.format(full_name))

    def add_person(self, first_name, last_name, role, wants_accommodation='N'):
        if role.upper() == 'FELLOW' and wants_accommodation.upper() == 'Y':
            new_fellow = Fellow(first_name, last_name)
            self.employees[new_fellow.name.title()] = role
            self.fellow.append(new_fellow.name.title())
            """randomly allocate office and living_space """
            random_office = Amity.generating_random_office(self)
            random_living_space = Amity.generating_random_living_space(self)

            """If person is not given an office or a living_space"""
            if not random_office and not random_living_space:
                self.unallocated_office[new_fellow.name.title()] = role
                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {} to the unallocated list'.format(new_fellow.name))

                """if person is not being allocated a random office  but
                            will be allocated a random living_space"""
            elif random_living_space and not random_office:
                self.unallocated_office[new_fellow.name.title()] = role
                print('Added: {} to the unallocated list' .format(new_fellow.name))
                self.living_space[random_living_space].append(new_fellow.name.title())
                print("Added: {} and allocated them to a living_space "
                      "{}: ".format(new_fellow.name, random_living_space))
                """If person is not being allocated a living_space but will be allocated an office"""
            elif random_office and not random_living_space:
                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {} to the unallocated list' .format(new_fellow.name))
                self.office[random_office].append(new_fellow.name.title())
                print("Added: {} and allocated them to an office {}: "
                      .format(new_fellow.name, random_office))

            else:
                """allocate person both office and living_space"""

                self.office[random_office].append(new_fellow.name.title())
                print("Added: {} and allocated them to {}: " .format(new_fellow.name, random_office))
                self.living_space.get(random_living_space).append(new_fellow.name.title())
                print("Added: {} and allocated them to {}: " .format(new_fellow.name, random_living_space))

        elif role.upper() == 'FELLOW':
            """if person is a fellow but selects no to receive living_space
            the default is No"""
            new_fellow = Fellow(first_name, last_name)
            self.employees[new_fellow.name.title()] = role
            self.fellow.append(new_fellow.name.title())
            random_office = Amity.generating_random_office(self)
            if not random_office:
                self.unallocated_office[new_fellow.name.title()] = role
                print('Added: {0} to the unallocated list' .format(new_fellow.name))
            else:
                self.office[random_office].append(new_fellow.name.title())
                print("Added: {0} and allocated them to {0}: ".format(new_fellow.name, random_office))

        elif role.upper() == 'STAFF' and wants_accommodation.upper() == 'Y':
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name.title()] = role
            self.staff.append(new_staff.name)
            random_office = Amity.generating_random_office(self)
            if not random_office:
                self.unallocated_office[new_staff.name.title()] = role
                print('Added: {0} to the unallocated list'.format(new_staff.name))
                print('Staff cannot be allocated a living_space')
            else:
                self.office[random_office].append(new_staff.name.title())
                print("Added: {0} and allocated them to {0}: " .format(new_staff.name, random_office))
                print('Staff cannot be allocated a living_space')

        elif role.upper() == 'STAFF':
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name.title()] = role
            self.staff.append(new_staff.name.title())
            random_office = Amity.generating_random_office(self)
            if not random_office:
                """allocate a random office to staff"""
                self.unallocated_office[new_staff.name.title()] = role
                print('Added: {0} to the unallocated list' .format(new_staff.name))
            else:
                self.office[random_office].append(new_staff.name.title())
                print("Added: {0} and allocated them to {0}: " .format(new_staff.name, random_office))

        else:
            print('{0} is not a valid role.' .format(role))

    def reallocate_person_to_office(self, first_name, last_name, room_name):
        full_name = first_name + " "+ last_name
        if not full_name in self.employees:
            print("{0} does not exist in the system".format(full_name))

        if len(self.office[room_name]) == 6:
            print(" {0} is full, please choose another room" .format(room_name))

        if full_name in self.office[room_name]:
            print("{0} is already in {0}".format(full_name,room_name))

        for room, occupants in self.office.items():
            if full_name in occupants:
                self.office[room].remove(full_name)
                self.office[room_name].append(full_name)
                print("{0} has been reallocated successfully  {0}".format(full_name,room_name))

    def reallocate_person_to_living_space(self, first_name, last_name, room_name):
        full_name = first_name + " "+ last_name
        if full_name not in self.employees:
            print("{0} does not exist in the system".format(full_name))

        if len(self.living_space[room_name]) == 4:
            print(" {0} is full, please choose another room" .format(room_name))

        if full_name in self.living_space[room_name]:
            print("{0} is already in {0}".format(full_name,room_name))

        for room, occupants in self.living_space.items():
            if full_name in occupants:
                self.living_space[room].remove(full_name)
                self.living_space[room_name].append(full_name)
                print("{0} has been reallocated successfully  {0}".format(full_name,room_name))

    def generating_random_office(self):
        """generates random offices to be allocated by the add person function"""
        self.vacant_office = [space for space in self.office if len(self.office[space]) < 6]

        if len(self.vacant_office) > 0:
            random_office = random.choice(self.vacant_office)
            return random_office

        else:
            print("No office available.Please try later")

    def generating_random_living_space(self):
        """generates random living spaces to be allocated by the add person function"""
        self.vacant_living_space = [space for space in self.living_space if len(self.living_space[space]) < 4]

        if len(self.vacant_living_space) > 0:
            random_living_space = random.choice(self.vacant_living_space)
            return random_living_space
        else:
            print('No living spaces available.Please try later')

    def print_rooms(self, room_name):
        """print all the members from a given room"""
        display_office = [office for office in self.office if office != "None"]
        display_living_spaces = [living_space for living_space in self.living_space if living_space != "None"]
        if room_name.title() not in display_office and room_name.title() not in display_living_spaces:
            print("The room does not exist. Please check you entered the correct entry")
        else:
            print("Occupants List")
            if room_name.title() in display_office:
                for person in self.office[room_name.title()]:
                    print(person)
            elif room_name.title() in display_living_spaces:
                for person in self.living_space[room_name.title()]:
                    print(person)

    def print_allocations(self, filename=None):
        """Prints all the people who have rooms"""

        for room in self.office.keys():
            if room != "None":
                print(room + "\n" + "+" * 30)
                for person in self.office[room]:
                    print(person)

        for room in self.living_space.keys():
            if room != "None":
                print(room + "\n" + "*" * 30)
                for person in self.living_space[room]:
                    print(person)

        if filename:
            print("-" * 30 + "\n" + "Office Allocations"+ "\n" + "-" * 30)
            file = open(filename + ".txt", "a")
            file.write("#" * 30 + "\n" + "Office"+"\n" + "#" * 30)

            print("-" * 30 + "\n" + "Living Space Allocations" + "\n"+ "-" * 30)
            for room in self.office.keys():
                if room != "None":
                    file.write(room + "\n" + "*" * 30)
                    for person in self.office[room]:
                        file.write(person)
            file.write("*" * 30 + "\n" + "Living Space" +"\n" + "*" * 30)
            for room in self.living_space.keys():
                if room != "None":
                    file.write(room + "\n" + "*" * 30)
                    for person in self.living_space[room]:
                        file.write(person)

            print("{0}.txt printed" .format(filename))

    def print_unallocated(self, filename):
        """Print unallocated in office"""
        for room in self.unallocated_office.keys():
            if room != "None":
                print(room + "\n" + "*" * 30)
                for person in self.unallocated_office[room]:
                    print(person)
        for room in self.unallocated_living_space.keys():
            if room != "None":
                print(room + "\n" + "*" * 30)
                for person in self.unallocated_living_space[room]:
                    print(person)
        if filename:
            print("*" * 60 + "\n" + "Unallocated members: Office Space\n" + "*" * 60)
            file = open(filename + ".txt", "a")
            file.write("*" * 30 + "\n" + "Office\n" + "*" * 30)

            print("*" * 60 + "\n" + "Unallocated members: Living Space"+ "\n" + "*" * 60)
            for room in self.unallocated_office.keys():
                if room != "None":
                    file.write(room + "\n" + "*" * 60)
                    for person in self.unallocated_office[room]:
                        file.write(person)
            file.write("*" * 60 + "\n" + "Living Space"+"\n" + "*" * 60)
            for room in self.unallocated_living_space.keys():
                if room != "None":
                    file.write(room + "\n" + "*" * 60)
                    for person in self.unallocated_living_space[room]:
                        file.write(person)

            print("{0}.txt printed" .format(filename))

    def load_people(self, filename):
        if filename:
            with open(filename) as amity_load:
                for each_line in amity_load:
                    details = each_line.split()
                    if len(details) == 4:
                        first_name = details[0]
                        last_name = details[1]
                        role = details[2]
                        wants_accommodation = details[3]
                        self.add_person(first_name, last_name, role, wants_accommodation)

                        if len(details) == 3:
                            first_name = details[0]
                            last_name = details[1]
                            role = details[2]
                            self.add_person(first_name, last_name, role)
                    else:
                        print('The file is not readable. ')
        else:
            print('Please ensure the file is valid')

    def load_rooms(self, filename):
        if filename:
            with open(filename, "r") as room_load:
                rooms = room_load.readlines()
                for each_line in rooms:
                    rooms = each_line.split()

                    if len(rooms) == 2:
                        room_type = rooms[0]
                        room_name = rooms[1]
                        self.create_room(room_type, [room_name])

                    else:
                        print('The file is not readable. ')
        else:
            print('Please ensure the file is valid')

    def load_state(self,db_name):
        if db_name:
            db_load = AmityDatabaseLoad(db_name)
        else:
            print("cannot find database")

        Base.metadata.bind = db_load.engine
        db_session = db_load.session

        people = select([PersonDB])
        result = db_load.session.execute(people)

        for person in result.fetchall():
            name = person.name
            role = person.role
            self.employees[name] = role
        db_session.close()

        """load rooms from database"""
        db_room = select([RoomDB])
        result = db_load.session.execute(db_room)
        for room in result.fetchall():
            name = room.room_name
            room_type = room.room_type
            self.room_directory[name] = room_type
        db_session.close()

        # load office allocations from database
        occupant_offices = select([OfficeDB])
        result = db_load.session.execute(occupant_offices)
        for office in result.fetchall():
            room_name = office.room_name
            occupant = office.occupants
            self.office[room_name]
            if occupant not in self.office[room_name]:
                self.office[room_name].append(occupant)
        db_session.close()

        # load living_space allocations from database
        occupant_living_space = select([LivingSpaceDB])
        result = db_load.session.execute(occupant_living_space)
        for living_space in result.fetchall():
            room_name = living_space.room_name
            occupant = living_space.occupants
            self.living_space[room_name]
            if occupant not in self.living_space[room_name]:
                self.living_space[room_name].append(occupant)
        db_session.close()
        # load unallocated people from database
        unallocated_person = select([UnallocatedDB])
        result = db_load.session.execute(unallocated_person)
        for person in result.fetchall():
            name = person.name
            if name not in self.unallocated_living_space:
                self.unallocated_living_space
            elif name not in self.unallocated_office.append(name):
                self.unallocated_office
        db_session.close()
        print(" {0} loaded successfully." .format(db_name))

    def save_state(self,db_name=None):
        if db_name:
            db_load = AmityDatabaseLoad("room_allocation_db")
        else:
            db_load = AmityDatabaseLoad(db_name)
        Base.metadata.bind = db_load.engine
        db_session = db_load.session()
        for room in self.room_directory:
            save_room = RoomDB(room_name=room.room_name, room_type=room.room_type, capacity=room.capacity)
            db_session.add(save_room)
            print(save_room)
            # room = self.room_directory[room_type]
            # room_name = self.room_directory[room_type][0]
            # capacity = self.room_directory[room_type][1]
            # room_data = RoomDB(room_name, room_type, )
        for person in self.employees:
            save_person = PersonDB(name=person.name, role=person.role)
            db_session.add(save_person)
        for room in self.office:
            office_occupants = ",".join(self.office[room])
            office_allocations_sv = OfficeDB(room_name=room, occupants=office_occupants)
            db_session.add(office_allocations_sv)
        for room in self.living_space:
            living_space_occupants = ",".join(self.living_space[room])
            living_space_saved = LivingSpaceDB(room_name=room,occupants=living_space_occupants)
            db_session.add(living_space_saved)

        db_session.commit()
        print("Saved!")

