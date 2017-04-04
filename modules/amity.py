
""" This is an application that models room allocation for Andela """
import os


class Amity(object):

    def __init__(self, **kwargs):
        self.new_room = {"room_type": "room_name"}
        self.emp_id = {"employee": "id"}
        self.office = []
        self.living_space = []
        self.office_allocation = {"emp_id": ["office_name"]}

    def __len__(self):
        return len([])
# Creates rooms in Amity

    def open_file(self):
        self.file_name = open('amity_load.txt', mode='r')
        self.file_list = self.file_name.readline()
        self.file_list.close()

        return

    def create_room(self, room_name, room_type):
        if self.room_type == self.office:
            return self.office.append()
        elif self.room_type == self.living_space:
            return self.living_space.append()

# allocate room type
    def choose_room_type(self, office, living_space, room_type):
        self.office = office
        self.living_space = living_space
        self.room_type = [office, living_space]
# enable user to choose the type of room to create
        for new_room in room_type:
            if new_room == office:
                return [self.office]
            elif new_room == living_space:
                return [self.living_space]
            else:
                return "Not a valid entry"

    def check_office_has_space(self):
        space = len(self.office)
        if space >= 6:
            return "No more space"
        else:
            return len(self.office)

    def check_living_space_has_space(self):
        space = len(self.living_space)
        if space >= 6:
            return "No more space"
        else:
            return len(self.living_space)

# view rooms

    def view_rooms(self):
        pass

# Reallocate the person with person_identifier to new_room_name.

    def reallocate_person(self):
        pass

# Prints a list of allocations

    def print_allocations(self):
        pass

# Prints a list of unallocated

    def print_unallocated(self):
        pass


class Room (Amity):
    def __init__(self, office, living_space):

        self.Office = office
        self.Living_space = living_space

    def load_people(self):
        load_people = os.path.join(os.path.dirname(__file__), 'amity_load.txt')
        load_data = open(load_people).read()
        load_data.close()
        return self









