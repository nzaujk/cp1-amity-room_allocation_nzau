"""this class contains the office and living space methods """


class Room(object):
    def __init__(self, room_name=None, room_type=None, capacity=None):
        self.room_name = room_name
        self.capacity = capacity
        self.room_type = room_type
        self.occupants = []


class Office(Room):
    """office inherits from base class super method runs before the subclass instance"""
    def __init__(self, room_name):
        super().__init__(room_name, room_type="office", capacity=6)


class LivingSpace(Room):
    """LivingSpace inherits from base class. super method runs before the subclass instance"""

    def __init__(self, room_name):
        super().__init__(room_name, room_type="living space", capacity=4)

