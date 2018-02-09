class Location(object):
    def __init__(self, location_dict):
        self.name = location_dict['name']
        self.address = location_dict['address']

    def __str__(self):
        return str(self.type.value)

    def pretty(self):
        return self.__str__()
