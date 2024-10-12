import random


class RouteSA():
    sequence = []
    total_distance = -1
    distance_matrix = None

    def __init__(self, distance_matrix, route_size=None, start = 0,stop = 1, sequence=None):
        self.distance_matrix = distance_matrix
        self.start = start
        self.stop = stop

        if route_size:
            self.create_random_sequence(route_size)
        elif sequence:
            self.sequence = sequence
        else:
            exit

        self.apply_2opt()

        self.total_distance = self.get_distance()

    def get_distance(self):
        total_distance = 0
        sequence = self.sequence
        total_distance += self.distance_matrix[self.start][sequence[0]-1]
        
        for i in range(0, len(sequence) - 1):
            total_distance += self.distance_matrix[sequence[i] - 1][sequence[i + 1] - 1]
        # total_distance += self.distance_matrix[0][sequence[-1] - 1]
        total_distance += self.distance_matrix[sequence[-1] - 1][self.stop]
        return total_distance
    
    def swap_two_cities(self):
        new_route = self.sequence[:]
        i, j = random.sample(range(1, len(self.sequence) - 1), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        self.sequence =new_route
        

        # self.apply_2opt()

        self.total_distance = self.get_distance()
        
    def apply_2opt(self):
        distance_matrix=self.distance_matrix
        
        n = len(self.sequence)
        new_sequence = self.sequence.copy()

        for i in range(0, n - 2):
            for j in range(i + 3, n):
                current_connection = (
                    distance_matrix[self.sequence[i] - 1][self.sequence[i + 1] - 1]
                    + distance_matrix[self.sequence[j - 1] - 1][self.sequence[j] - 1]
                )

                reversed_connection = (
                    distance_matrix[self.sequence[i] - 1][self.sequence[j - 1] - 1]
                    + distance_matrix[self.sequence[i + 1] - 1][self.sequence[j] - 1]
                )

                if reversed_connection < current_connection:
                    new_sequence[i + 1 : j] = self.sequence[j - 1 : i : -1].copy()
                    self.sequence = new_sequence.copy()
                    self.total_distance = self.get_distance()

 
    def create_random_sequence(self, route_size):
        self.sequence = list(range(1, route_size + 1))
        self.sequence = [city for city in self.sequence if city != (self.start + 1) and city != (self.stop + 1)]
        random.shuffle(self.sequence)