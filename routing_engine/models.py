class BusStop:

    def __init__(self, name, prev=None, next=None):
        """
        Represents bus stop, and have links to all previous
        and next bus stops
        :param name: str
        :param prev: list[BusStop]
        :param next: list[BusStop]
        """

        self.name = name
        self.prev = prev
        self.next = next

    def __str__(self):
        return self.name

    def __eq__(self, other):
        """
        If 2 stops have the same name - they are equals
        Should be changed to geo-coordinates for example
        """
        return self.name == other.name

    def __hash__(self):
        return id(self)


class Bus:

    _all = []

    @classmethod
    def get_buses_in_stop(cls, bus_stop):
        buses = set()
        for bus in cls._all:
            for stop in bus.bus_stopes:
                if stop.name == bus_stop.name:
                    buses.add(bus)
                    break
        return buses

    def __init__(self, name, bus_stopes):
        """
        Represent a bus route. Stores list of all stopes
        in correct order
        :param name: str
        :param bus_stopes: list[BusStop]
        """
        self.name = name
        self.bus_stopes = bus_stopes
        # store all bus routes in class var
        self._all.append(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return id(self)


class Path:
    """
    Class which will save the route from point A to point B
    """

    def __init__(self, prev_path, current_stop):
        self.prev_path = prev_path
        self.current_stop = current_stop

    def get_string_path(self):
        """
        Return path with BusStops
        example: "ABCDE"
        :return: str
        """
        path_string = ""
        path = self
        while path:
            path_string += path.current_stop.name
            path = path.prev_path
        return path_string
