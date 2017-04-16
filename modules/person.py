

class Person(object):
    def __init__(self, first_name, last_name, role=None):
        self.name = first_name + " " + last_name
        self.role = role


class Fellow(Person):
    def __init__(self,first_name, last_name):
        super().__init__(first_name,last_name, role="Fellow")


class Staff(Person):
    def __init__(self, first_name, last_name):
        super().__init__(first_name,last_name, role='Staff')