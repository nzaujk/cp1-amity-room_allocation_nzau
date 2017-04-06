import os


class Person(object):
    def __init__(self):
        self.emp_id = []
        self.name = []

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
    # Adds a person to the system and allocates the person to a random room.
    def add_fellow(self, emp_id, name):
        self.emp_id = []
        self.name =[]
        directory = {self.emp_id: self.name}

        for fellow in directory:
            if emp_id and name not in directory:
                self.emp_id.append
                self.name.append
                directory.add()
                self.file_name = open('amity_load.txt', mode='w')
                self.file_name.close()
                return fellow
            else:
                return "fellow already exists"

    def is_fellow(self, emp_id, name):
        #determine if is fellow
        self.emp_id = [emp_id]
        self.name =[name]
        directory = [{emp_id: name}]
        for emp_id, name in directory:
            if emp_id and name is True:
                return 'is fellow'
            else:
                return "not fellow"


class Staff(Person):
    def add_staff(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name
        directory = set({emp_id: name})
        for staff in directory:
            if emp_id and name not in directory:
                self.emp_id.append
                self.name.append
                directory.add()
                self.file_name = open(os.path.dirname(__file__), 'amity_load.txt', mode='w')
                self.file_name.close()
                return staff
            else:
                return "staff already exists"

    def is_staff(self, emp_id, name):
        # functions to determine if is staff
        self.emp_id = [emp_id]
        self.name = [name]
        directory = [{emp_id: name}]
        for emp_id, name in directory:
            if emp_id and name is True:
                return 'is staff'
            else:
                return "not staff"
