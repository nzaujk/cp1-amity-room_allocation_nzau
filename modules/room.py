from modules.amity import Room


class Office(Room):
    def __init__(self, maximum = 6, occupants = 0, available = 6):
        self.maximum = maximum
        self.occupants = occupants
        self.available = available

    def occupants(self, occupied):
        self.occupied = len(self.occupants)
        return occupied

    def available(self,):
        pass


class LivingSpace(Room):
    def __init__(self):
        pass

    def capacity(self):
        pass
