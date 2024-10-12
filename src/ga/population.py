# from localtileserver import get_folium_tile_layer, TileClient
# tile_client = TileClient(fileNameGeoTIFF)
# foliumMap = folium.Map(
#                 location=tile_client.center(),
#                 tiles=None, zoom_start=10,max_zoom=15,min_zoom=1, 
#                 )
# tile_layer = get_folium_tile_layer(tile_client, name='test',
#                         control=True,
#                         overlay=True)
# foliumMap.add_child(tile_layer)


from ga.route import RouteGA

import random


class PopulationGA():
    __instance = None
    route_list = []  
    current_generation = -1
    route_size = None
    distance_matrix = None
    best_route = None
    best_distance = None
    mutation_percent = 0.01
    pop_size = -1
    number_of_children = -1

    def __init__(
        self,
        pop_size,
        route_size,
        number_of_children,
        distance_matrix,
        mutation_percent,
        start,
        stop
    ):
        self.pop_size = pop_size
        self.route_size = route_size
        self.number_of_children = number_of_children
        self.distance_matrix = distance_matrix
        self.mutation_percent = mutation_percent
        self.start= start
        self.stop = stop
        if PopulationGA.__instance != None:
            raise NotImplemented("This is a singleton class.")

        # Generate random population in given number
        for _ in list(range(pop_size)):
            self.route_list.append(
                RouteGA(distance_matrix=distance_matrix, route_size=route_size, start=start,stop=stop)
            )

        self.sort()
        self.best_route = self.route_list[0]
        self.best_distance = self.best_route.total_distance
        self.current_generation = 0

    def parent_selection(self):
        parent_count = self.number_of_children * 2
        parent_list = []

        max_random = (self.pop_size * (self.pop_size + 1)) / 2

        for i in range(0, parent_count):
            k = 1
            random_value = random.randint(1, max_random)
            for j in range(0, self.pop_size):
                if random_value <= k:
                    parent_list.append(self.pop_size - j - 1)  # Reverse
                    break

                k = k + j + 2  # The next cumulative limit
        return parent_list

    def iterate_generation(self):
        parent_list = self.parent_selection()

        for i in range(0, self.number_of_children * 2, 2):
            route1 = self.route_list[parent_list[i]]
            route2 = self.route_list[parent_list[i + 1]]

            new_route = RouteGA.crossover(route1, route2, self.distance_matrix, self.start, self.stop)

            if new_route in self.route_list:
                pass
            else:
                self.route_list.append(new_route)

        # Mutation 
        random_value = random.random()
        if random_value < self.mutation_percent:
            selected_route = self.route_list[random.randint(0, self.pop_size - 1)]
            new_sequence = RouteGA.mutation(selected_route.sequence)
            new_route = RouteGA(
                distance_matrix=self.distance_matrix, sequence=new_sequence, start = self.start, stop = self.stop
            )
            self.route_list.append(new_route)

        # After adding new routes, sort all and remove surplus.
        self.sort()
        self.route_list = self.route_list[0 : self.pop_size]

        new_route = self.route_list[0]
        new_best_distance = self.route_list[0].total_distance

        improved_flag = False  # Flag for showing improvement

        if new_best_distance < self.best_distance:
            improved_flag = True
            self.best_distance = new_best_distance
            self.best_route = new_route

        self.current_generation += 1
        return improved_flag

    def sort(self):
        self.route_list = sorted(
            self.route_list, key=lambda route: route.total_distance
        )