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


import math
from sa.route import RouteSA

import random


class PopulationSA():
    __instance = None
    route_list = []  
    current_generation = -1
    route_size = None
    distance_matrix = None
    best_route = None
    best_distance = None
    pop_size = -1
    number_of_children = -1
    
    T =  None
    T_min  =None
    alpha = None


    def __init__(
        self,
        max_generation,
        pop_size,
        route_size,
        number_of_children,
        distance_matrix,
        start,
        stop,
        T = 1000.0,
        T_min= 0.00001,
        alpha= 0.995
    ):
        self.max_generation= max_generation
        self.pop_size = pop_size
        self.route_size = route_size
        self.number_of_children = number_of_children
        self.distance_matrix = distance_matrix
        self.start= start
        self.stop = stop
        self.T = T
        self.T_min = T_min
        self.alpha = alpha


        if PopulationSA.__instance != None:
            raise NotImplemented("This is a singleton class.")

        # Generate random population in given number
        for _ in list(range(pop_size)):
            self.route_list.append(
                RouteSA(distance_matrix=distance_matrix, route_size=route_size, start=start,stop=stop)
            )

        self.sort()
        self.best_route = self.route_list[0]
        self.best_distance = self.best_route.total_distance
        self.current_generation = 0


    
    def simulated_annealing(self):
        current_route = self.best_route
        current_distance = self.best_distance
        best_route = current_route
        best_distance = current_distance
        T = self.T
        T_min = self.T_min
        alpha = self.alpha

        while self.current_generation < self.max_generation and T > T_min:
            route = RouteSA(distance_matrix=self.distance_matrix,
                          route_size=self.route_size, 
                          start=self.start,
                          stop=self.stop,
                          sequence=current_route)
            
            route.swap_two_cities()
            try:
                acceptance_prob = math.exp((current_distance - route.total_distance) / T)            
                if route.total_distance < current_distance or random.random() < acceptance_prob:
                    current_route = route.sequence
                    current_distance = route.total_distance
                
                if route.total_distance < best_distance:
                    best_route = route.sequence
                    best_distance = route.total_distance
            except:
                print(acceptance_prob, route.total_distance, current_distance)
                
            T *= alpha
            
            self.current_generation += 1
        
        return best_route, best_distance
 

    def sort(self):
        self.route_list = sorted(
            self.route_list, key=lambda route: route.total_distance
        )