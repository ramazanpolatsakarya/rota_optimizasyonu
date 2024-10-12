import random


class RouteGA():
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
    


    def apply_2opt(self):
        distance_matrix = self.distance_matrix
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

    def crossover(route1, route2, distance_matrix,start,stop):
        sequence1 = route1.sequence
        sequence2 = route2.sequence
        sequence_length = len(sequence1)

        # selected_number = random.randint(1, sequence_length)  # Starting point
        selected_number = random.choice(sequence1)  # Starting point

        sequence1_index = sequence1.index(selected_number)
        sequence2_index = sequence2.index(selected_number)

        # Continue adding numbers until False
        sequence1_flag = True
        sequence2_flag = True

        # Empty route
        new_sequence = [0] * sequence_length

        new_sequence[0] = selected_number

        cursor_forward = 1
        cursor_backward = sequence_length - 1

        while sequence1_flag == True or sequence2_flag == True:
            if sequence1_flag == True:
                # Take the index to the beginning point if it is at the finish
                if sequence1_index == sequence_length - 1:
                    sequence1_index = 0
                else:
                    sequence1_index += 1

                # Is next value added? Then change flag to False
                # Else add next value to list
                if sequence1[sequence1_index] in new_sequence:
                    sequence1_flag = False
                else:
                    new_sequence[cursor_forward] = sequence1[sequence1_index]
                    cursor_forward += 1
            if sequence2_flag == True:
                # Take the index to the finish point if it is at the beginning
                if sequence2_index == 0:
                    sequence2_index = sequence_length - 1
                else:
                    sequence2_index -= 1

                # Is the next value added before? If yes, change the flag to False
                # Else add the next value to the list
                if sequence2[sequence2_index] in new_sequence:
                    sequence2_flag = False
                else:
                    new_sequence[cursor_backward] = sequence2[sequence2_index]
                    cursor_backward -= 1

        remaining_numbers = [x for x in sequence1 if x not in new_sequence]
        random.shuffle(remaining_numbers)

        for i in range(len(remaining_numbers)):
            new_sequence[cursor_forward] = remaining_numbers[i]
            cursor_forward += 1

        return RouteGA(distance_matrix=distance_matrix, sequence=new_sequence, start=start, stop=stop)

    def mutation(sequence):
        size = len(sequence)
        selected_number = random.choice(sequence)
        random_index = random.randint(0, size - 1)
        new_sequence = list(sequence)
        new_sequence.remove(selected_number)
        new_sequence.insert(random_index, selected_number)
        return new_sequence

    def create_random_sequence(self, route_size):
        self.sequence = list(range(1, route_size + 1))
        self.sequence = [city for city in self.sequence if city != (self.start + 1) and city != (self.stop + 1)]
        random.shuffle(self.sequence)