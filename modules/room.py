from modules.amity import Amity


class Office(Amity):
    def __init__(self, maximum = 6, available = 6):
        self.maximum = maximum
        self.available = available

    def create_room(self, room_type, room_name):
        self.room_type = ['office']
        self.room_name = []
        for name in self.room_name:
            if name != self.room_name:
                return[{self.room_type: [self.room_name.append]}]
            else:
                return 'name already exists'

    def view_office(self):
        for office in self.room_type:
            if self.room_type is [self.office]:
                office.append()
                return set(office)
            else:
                return []

    def view_available(self):
        self.available = 6
        size = len(self.available)
        if size > 6:
            return "no more space"
        else:
            return size


class LivingSpace(Amity):
    def __init__(self):
        self.occupants = 0
        self.available = 4

    def create_room(self, room_type, room_name):
        self.room_type = ['living_space']
        self.room_name = []
        for name in self.room_name:
            if name != self.room_name:
                return[{self.room_type: [self.room_name.append]}]
            else:
                return 'name already exists'

    def view_ls(self):
        for living_space in self.room_type:
            if self.room_type is [self.living_space]:
                living_space.append()
                return set(living_space)
            else:
                return []

    def view_available(self):
        self.available = 4
        size = len(self.available)
        if size > 4:
            return "no more space"
        else:
            return size


