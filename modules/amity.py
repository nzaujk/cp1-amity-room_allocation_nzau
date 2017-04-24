
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
        self.room_directory = defaultdict(list)
        self.vacant_office = []
        self.vacant_living_space = []
        self.unallocated_office = {}
        self.unallocated_living_space = {}
        self.staff = []
        self.fellow = []
        self.employees = {}
        self.living_space = {}
        self.office = {}

    def create_room(self, room_type, room_name):
        """Check room does not exist."""
        for room in room_name:
            if room in self.office or room in self.living_space:
                print("The room Exists")
                return "operation not successful"

            if room_type == 'office':
                new_office = Office(room)
                self.room_directory[new_office.room_name.title()] = new_office.room_type
                self.office[room] = new_office
                print("{}: {} has been successfully created!".format(room_type, new_office.room_name))
                return "operation successful"

            elif room_type == 'living_space':
                new_living_space = LivingSpace(room)
                self.room_directory[new_living_space.room_name.title()] = new_living_space.room_type
                self.living_space[room] = new_living_space
                print("{}: {} has been successfully created!".format(room_type, new_living_space.room_name))
                return "operation successful"

    def add_person(self, first_name, last_name, role, wants_accommodation='n'):
        """Adds a person into the system"""
        full_name = first_name.title() + " " + last_name.title()
        if full_name in self.employees:
            print('{} is already in the system.'.format(full_name))
            return "operation not successful"

        if role.lower() == 'fellow' and wants_accommodation.lower() == 'y':
            new_fellow = Fellow(first_name, last_name)
            self.employees[new_fellow.name] = role
            self.fellow.append(new_fellow.name)

            """randomly allocate office and living_space """
            random_office = Amity.generating_random_office(self)
            random_living_space = Amity.generating_random_living_space(self)

            """If person is not given an office or a living_space"""
            if not random_office and not random_living_space:
                self.unallocated_office[new_fellow.name.title()] = role
                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {} to the unallocated list'.format(new_fellow.name))
                return "Operation not successful.Added to unallocated"

                """if person is not being allocated a random office  but
                            will be allocated a random living_space"""
            elif random_living_space and not random_office:
                self.unallocated_office[new_fellow.name.title()] = role
                print('Added: {} to the unallocated list' .format(new_fellow.name))
                self.living_space[random_living_space].occupants.append(new_fellow.name.title())
                print("Added: {} and allocated them to a living_space "
                      "{}: ".format(new_fellow.name, random_living_space))
                return "operation successful but added to unallocated list"

                """If person is not being allocated a living_space but will be allocated an office"""

            elif random_office and not random_living_space:
                self.unallocated_living_space[new_fellow.name.title()] = role
                print('Added {} to the unallocated list' .format(new_fellow.name))
                self.office[random_office].occupants.append(new_fellow.name)
                print("Added: {} and allocated them to an office {}".format(new_fellow.name, random_office))
                return "operation successful but added to unallocated list"

            else:
                """allocate person both office and living_space"""
                self.office[random_office].occupants.append(new_fellow.name.title())
                print("Added: {} and allocated them to {}  office" .format(new_fellow.name, random_office))
                self.living_space[random_living_space].occupants.append(new_fellow.name.title())
                print("Added: {} and allocated them to {} living_space " .format(new_fellow.name, random_living_space))
                return "operation successful"
        # added accommodations = n
        elif role.lower() == 'fellow' and wants_accommodation=="n":
            """if person is a fellow but selects no to receive living_space
            the default is No"""
            new_fellow = Fellow(first_name, last_name)
            self.employees[new_fellow.name] = role
            self.fellow.append(new_fellow.name)
            random_office = Amity.generating_random_office(self)
            if not random_office:
                self.unallocated_office[new_fellow.name.title()] = role
                print('Added: {0} to the unallocated list' .format(new_fellow.name))
                return "operation successful:unallocated list"
            else:
                self.office[random_office].occupants.append(new_fellow.name.title())
                print("Added: {} and allocated them to {} office ".format(new_fellow.name, random_office))
                return "operation successful"

        elif role.lower() == 'staff' and wants_accommodation.lower() == 'y':
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name.title()] = role
            self.staff.append(new_staff.name.title())
            random_office = Amity.generating_random_office(self)
            if not random_office:
                self.unallocated_office[new_staff.name.title()] = role
                print('Added: {0} to the unallocated list'.format(new_staff.name))
                print('Staff cannot be allocated a living_space')
                return "Added to unallocated list. Living space allocation not successful"
            else:
                self.office[random_office].occupants.append(new_staff.name.title())
                print("Added: {} and allocated them to {} office " .format(new_staff.name, random_office))
                print('Staff cannot be allocated a living_space')
                return "Office allocation successful. Living space allocation not successful"

        elif role.lower() == 'staff':
            new_staff = Staff(first_name, last_name)
            self.employees[new_staff.name] = role
            self.staff.append(new_staff.name)
            random_office = Amity.generating_random_office(self)
            if not random_office:

                self.unallocated_office[new_staff.name.title()] = role
                print('Added: {0} to the unallocated list' .format(new_staff.name))
                return "Office not successful.Added to unallocated list"
            else:
                """allocate a random office to staff"""
                self.office[random_office].occupants.append(new_staff.name.title())
                print("Added: {} and allocated them to {} office " .format(new_staff.name, random_office))
                return "operation successful"

        else:
            print('{0} is not a valid role.' .format(role))
            return "not a valid role"

    def reallocate_person_to_office(self, first_name, last_name, room_name):
        full_name = first_name.title() + " " + last_name.title()
        if full_name not in self.fellow and full_name not in self.staff:
            print("{0} does not exist in the system".format(full_name))
            return "operation not successful.room does not exist"

        if len(self.office[room_name].occupants) == 6:
            print("{0} is full, please choose another room" .format(room_name))
            return "operation not successful.room is full"
        if full_name in self.office[room_name].occupants:
            print("{} is already in {}".format(full_name,room_name))
            return "operation not successful.reallocating to same place"

        for room in self.office:
            if full_name in self.office[room].occupants:
                self.office[room].occupants.remove(full_name)

        self.office[room_name].occupants.append(full_name)
        print("{} has been reallocated successfully  {}".format(full_name,room_name))
        return "operation successful"

    def reallocate_person_to_living_space(self, first_name, last_name, room_name):
        full_name = first_name + " "+ last_name
        if full_name not in self.fellow and full_name not in self.staff:
            print("{0} does not exist in the system".format(full_name))
            return "operation not successful.room does not exist"

        if len(self.living_space[room_name].occupants) == 4:
            print(" {0} is full, please choose another room" .format(room_name))
            return "operation not successful.room is full"

        if full_name in self.living_space[room_name].occupants:
            print("{} is already in {}".format(full_name,room_name))
            return "operation not successful.reallocating to same place"

        for room in self.living_space:
            if full_name in self.living_space[room].occupants:
                self.living_space[room].occupants.remove(full_name)

        self.living_space[room_name].occupants.append(full_name)
        print("{} has been reallocated successfully  {}".format(full_name,room_name))
        return "operation successful"

    def generating_random_office(self):
        """generates random offices to be allocated by the add person function"""
        self.vacant_office = [space for space in self.office if len(self.office[space].occupants) < 6]

        if self.vacant_office:
            random_office = random.choice(self.vacant_office)
            return random_office

        else:
            print("No office available.Please try later")

    def generating_random_living_space(self):
        """generates random living spaces to be allocated by the add person function"""
        self.vacant_living_space = [space for space in self.living_space if len(self.living_space[space].occupants) < 4]

        if self.vacant_living_space:
            random_living_space = random.choice(self.vacant_living_space)
            return random_living_space
        else:
            print('No living spaces available.Please try later')

    def print_rooms(self, room_name):
        """print all the members from a given room"""
        display_office = [office.title() for office in self.office if office != ""]
        display_living_spaces = [living_space.title() for living_space in self.living_space if living_space != ""]
        all_display_spaces = display_living_spaces + display_office
        try:
            if room_name.title() not in all_display_spaces:
                print("The room does not exist. Please check you entered the correct entry")
                return "room does not exist"
            else:
                print("Occupants List")
                if room_name.title() in display_office:
                    for person in self.office[room_name].occupants:
                        print(person)

                elif room_name.title() in display_living_spaces:
                    for person in self.living_space[room_name].occupants:
                        print(person)
        except:
            return "Invalid"

    def print_allocations(self, filename=None):
        """Prints all the people who have rooms"""
        room = ""
        for room in self.office:

            if room:
                for person in self.office[room].occupants:
                    print("+" * 30)
                    print(room + ": \t" + person + " \n")
                    print("+" * 30)
                print("\n")

        for room in self.living_space:

            # print(room + "\n" + "*" * 30)
            if room:
                for person in self.living_space[room].occupants:
                    print("+" * 30)
                    print(room + ": \t" + person + " \n")
                    print("+" * 30)
                print("\n")
        if not room:
            print("\n There are no allocations yet in the system")

        if filename:
            print("-" * 30 + "\n" + "Office Allocations"+ "\n" + "-" * 30)
            file = open(filename + ".txt", "w")
            file.write("#" * 30 + "\n" + "Office"+"\n" + "#" * 30)

            print("-" * 30 + "\n" + "Living Space Allocations" + "\n"+ "-" * 30)
            for room in self.office:
                file.write(room + ": \t" +"\n" + "*" * 30)
                if room:
                    for person in self.office[room].occupants:
                        file.write("\n"+ room + ": \t" + person + "\n")
            file.write("*" * 30 + "\n" + "Living Space" +"\n" + "*" * 30)
            for room in self.living_space:
                # if room != "None":
                file.write(room + "\n" + "*" * 30)
                if room:
                    for person in self.living_space[room].occupants:
                        file.write("\n" + room + ": \t" + person + "\n")

            print("{0}.txt printed" .format(filename))

    def print_unallocated(self, filename=None):
        """Print unallocated in office"""
        room =""
        for room in self.unallocated_office:
            # print(room + "\n" + "*" * 30)
            if room:
                for person in self.unallocated_office[room]:
                    print("+" * 30)
                    print(room + ": \t" + person + " \n")
                    print("+" * 30)
                print("\n")

        for room in self.unallocated_living_space:
            # print(room + "\n" + "*" * 30)
            if room:
                for person in self.unallocated_living_space[room]:
                    print("+" * 30)
                    print(room + ": \t" + person + " \n")
                    print("+" * 30)
                print("\n")
        if not room:
            print("\n The list is empty")
        if filename:
            print("*" * 30 + "\n" + "Unallocated members: Office Space\n" + "*" * 30)
            file = open(filename + ".txt", "w")
            file.write("*" * 30 + "\n" + "Office\n" + "*" * 30)
            print("*" * 30 + "\n" + "Living Space Allocations" + "\n" + "*" * 30)
            print("*" * 30 + "\n" + "Unallocated members: Living Space" + "\n" + "*" * 30)
            for room in self.unallocated_office[room].occupants:

                if room != "":
                    file.write(room + "\n" + "*" * 60)
                    for person in self.unallocated_office[room]:
                        file.write(person)
            file.write("*" * 30 + "\n" + "Living Space"+"\n" + "*" * 30)

            for room in self.unallocated_living_space[room].occupants:

                if room != "":
                    file.write(room + "\n" + "*" * 30)
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
                        accommodation = details[3]
                        self.add_person(first_name, last_name, role, wants_accommodation=accommodation)

                    if len(details) == 3:
                        first_name = details[0]
                        last_name = details[1]
                        role = details[2]
                        self.add_person(first_name, last_name, role, wants_accommodation='n')

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
                        print('The file is not readable.')

        else:
            print('Please ensure the file is valid')
            return "invalid file"

    def load_state(self,db_name):
        if db_name:
            db_load = AmityDatabaseLoad(db_name)
        else:
            db_load = AmityDatabaseLoad("amity_room_allocation")

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
        return "operation successful"

    def save_state(self, db_name='amity_db'):
        if db_name:
            db_load = AmityDatabaseLoad(db_name)
        else:
            db_load = AmityDatabaseLoad('amity__db')

        Base.metadata.bind = db_load.engine

        db_session = db_load.session

        # save people to database
        person_in_db = select([PersonDB])
        result = db_session.execute(person_in_db)
        people_list = [item.name for item in result]

        for full_name, role in self.employees.items():
            if full_name not in people_list:
                new_person = PersonDB(name=full_name, role=role)
                db_load.session.merge(new_person)
                db_load.session.commit()
        # saves the rooms to database
        rooms_in_db = select([RoomDB])
        result = db_load.session.execute(rooms_in_db)
        rooms_list = [item.room_name for item in result]

        for room, room_type in self.room_directory.items():
            if room not in rooms_list:
                new_name = RoomDB(room_name=room, room_type=room_type)
                db_load.session.merge(new_name)
                db_load.session.commit()

        # saves the people in offices
        person_in_office = select([OfficeDB])
        result = db_load.session.execute(person_in_office)
        office_occupants_list = [person.occupants for person in result]

        for room,people in self.office.items():
            for occupant in people.occupants:
                if occupant not in office_occupants_list:
                    room_name = OfficeDB(room_name=room, occupants=occupant)
                    db_load.session.add(room_name)
                    db_load.session.commit()
                    print("Data Saved")
                return "saved status"
        # save people in living_space
        person_in_living_space = select([LivingSpaceDB])
        result = db_load.session.execute(person_in_living_space)
        living_space_occupants_list = [person.occupants for person in result]
        for room, people in self.living_space.items():
            for occupant in people.occupants:
                if occupant not in living_space_occupants_list:
                    new_room = LivingSpaceDB(room_name=room, occupants=occupant)
                    db_load.session.add(new_room)
                    db_load.session.commit()


        # saves the fellow who are not allocated a livingspace
        unallocated_people = select([UnallocatedDB])
        result = db_load.session.execute(unallocated_people)
        unallocated_people_list = [person.name for person in result]
        for person in self.unallocated_living_space:
            if person not in unallocated_people_list:
                room_name = UnallocatedDB(name=person)
                db_load.session.add(room_name)
                db_load.session.commit()
                print("saved")
            return "saved status"

