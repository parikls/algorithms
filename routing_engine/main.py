from routing_engine.engine import Engine

from routing_engine.models import BusStop, Bus


def main():
    a = BusStop("A")
    b = BusStop("B")
    c = BusStop("C")
    d = BusStop("D")
    e = BusStop("E")
    f = BusStop("F")
    g = BusStop("G")
    h = BusStop("H")
    j = BusStop("J")
    a.next = [b, j]
    b.prev = [a, j]
    b.next = [c, g]
    c.prev = [b, e]
    c.next = [f, d]
    d.prev = [c, e]
    d.next = [h]
    f.prev = [c, g]
    f.next = [h]

    e.next = [c, d]
    e.prev = [j]
    g.next = [f]
    b.prev = [b]
    h.prev = [f, d]
    j.next = [b, e]
    j.prev = [a]

    bus_1 = Bus("bus number 1", [a, b, c, d])
    bus_2 = Bus("bus number 2", [e, c, f, h])
    bus_3 = Bus("bus number 3", [j, b, g, f, h])
    bus_4 = Bus("bus number 4", [a, j, e, d, h])

    [print(route) for route in Engine.build_routes(j, d)]


if __name__ == '__main__':
    main()
