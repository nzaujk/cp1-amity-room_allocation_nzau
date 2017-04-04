import os


class Person(object):
    def __init__(self, **kwargs):
        pass

# Adds a person to the system and allocates the person to a random room.
    def add_person(self, emp_id, name):
        self.file_name = open(os.path.dirname(__file__), 'amity_load.txt', mode='w').read()
        self.file_name.close()
        self.emp_id = []
        self.name = []
        self.add_person({self.emp_id: self.name})

    def allocate_person(self):
        pass

    def view_allocated(self):
        self.file_name = open('amity_load.txt', mode='r')
        self.file_list = self.file_name.readline()
        self.file_list.close()
        return

    def load_people(self):
        pass

    def reallocate_person(self):
        pass


class Fellow(Person):
    def __init__(self):
        pass

    def add_fellow(self):
        pass

    def is_fellow(self):
        # functions to determine if is fellow
        pass


class Staff(Person):
    def __init__(self):
        pass

    def add_staff(self):
        pass

    def is_staff(self):
        # functions to determine if is fellow
        pass
