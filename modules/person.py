
class Person(object):
    def __init__(self,first_name, last_name, role):
        self.name = first_name.title() + " " + last_name.title()
        self.role = role.lower()


class Fellow(Person):
    """fellow inherits from base class super method runs before the subclass instance"""
    def __init__(self, first_name, last_name):
        super().__init__(first_name,last_name, role="fellow")


class Staff(Person):
    """person inherits from base class super method runs before the subclass instance"""
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name, role="staff")

