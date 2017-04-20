

class Person(object):
    # def __init__(self, first_name, last_name, role=None):
    #     self.name = first_name + " " + last_name
    #     self.role = role
    def __init__(self):
        self.name = ""
        self.role = ""

class Fellow(Person):
    def __init__(self, first_name, last_name):
        # super().__init__()
        self.name = first_name.upper() + " " + last_name.upper()
        self.role = "fellow"


class Staff(Person):
    def __init__(self, first_name, last_name):
        # super().__init__()
        self.name = first_name.upper() + " " + last_name.upper()
        self.role = "staff"
