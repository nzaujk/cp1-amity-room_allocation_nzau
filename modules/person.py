

class Person(object):
    # def __init__(self, first_name, last_name, role=None):
    #     self.name = first_name + " " + last_name
    #     self.role = role
    def __init__(self,first_name, last_name, role):
        self.name = first_name.title() + " " + last_name.title()
        self.role = role.lower()


class Fellow(Person):
    def __init__(self, first_name, last_name):
        super().__init__(first_name,last_name, role="fellow")
        # self.name = first_name.title() + " " + last_name.title()
        # self.role = "fellow"


class Staff(Person):
    def __init__(self, first_name, last_name):
        # super().__init__()
        self.name = first_name.title() + " " + last_name.title()
        self.role = "staff"
