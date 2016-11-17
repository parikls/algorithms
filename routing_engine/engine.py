import queue

from routing_engine.models import Path, Bus


class Engine:
    """
    Main logic of building routes
    """

    def __new__(cls, *args, **kwargs):
        raise NotImplemented()

    @classmethod
    def build_routes(cls, stop_start, stop_end):
        """
        Returns routes in format:
        [(point1, point2), (bus1,)]
        :param stop_start: BusStop
        :param stop_end: BusStop
        :return: list[ (tuple, tuple,), ]
        """
        routes = []
        paths = cls._get_valid_paths(stop_start, stop_end)

        for path in paths:
            route = cls._construct_route(path)
            if route:
                route.reverse()
                routes.append(route)

        return routes


    @classmethod
    def _construct_route(cls, path):
        route = []
        while path:
            buses = Bus.get_buses_in_stop(path.current_stop)

            if path.prev_path:
                prev_buses = Bus.get_buses_in_stop(path.prev_path.current_stop)
                shared_buses = buses & prev_buses
                if not shared_buses:
                    return
                route.append(((path.prev_path.current_stop.name, path.current_stop.name,), shared_buses))
            else:
                # this is our start bus stop, it doesn't have previous bus stop
                next_buses = route[-1][-1]
                shared_buses = buses & next_buses
                if not shared_buses:
                    return
                route.append(((path.current_stop.name, ), (shared_buses,)))
            path = path.prev_path
        return route


    @classmethod
    def _get_valid_paths(cls, stop_start, stop_end):
        """
        Get all valid path using Breadth First Search
        :param stop_start: BusStop
        :param stop_end: BusStop
        :return: list[models.Path]
        """

        q = queue.Queue()
        # storage for all valid paths
        valid_paths = []
        start_path = Path(prev_path=None, current_stop=stop_start)

        q.put(start_path)

        while not q.empty():
            current_path = q.get()

            if current_path.current_stop == stop_end:
                # valid path is found!
                valid_paths.append(current_path)
                continue

            # if stop has next stopes
            if current_path.current_stop.next:
                for next_stop in current_path.current_stop.next:
                    path = Path(prev_path=current_path, current_stop=next_stop)
                    q.put(path)

        return valid_paths
