import time

from base.BaseTSP import BaseTSP
from ga.population import PopulationGA
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


class GA_TSP(BaseTSP):
    population = None
    pop_size = -1
    number_of_children = -1
    max_generation = 0
    current_generation = -1
    mutation_percent = 0.05
    parent_list = []

    result = Signal(PopulationGA)

    def __init__(self,data_path):
        
        super().__init__(data_path)
        

    def set_problem(
        self, pop_size, number_of_children, max_generation, mutation_percent, start,stop
    ):
        self.pop_size = pop_size
        self.number_of_children = number_of_children
        self.max_generation = max_generation
        self.mutation_percent = mutation_percent
        self.route_size = len(self.data.dataset)
        self.start = start
        self.stop = stop
        self.current_generation = 0

        self.population = PopulationGA(
            self.pop_size,
            self.route_size,
            self.number_of_children,
            self.data.distance_matrix,
            self.mutation_percent,
            self.start,
            self.stop
        )

    def start_ga_thread(self):
        # print(f"progress_callback = {progress_callback}")
        
        while  (
            self.population.current_generation < self.max_generation
        ):
            self.population.iterate_generation() 
        
        #işlem sonunda rotayı göndersin
        self.result.emit(self.population)
       
    def start_ga(self, fn):
        # print(f"progress_callback = {progress_callback}")
        
        while  (
            self.population.current_generation < self.max_generation
        ):   
            self.population.iterate_generation()
            # self.result.emit(self.population)
        
        #işlem sonunda rotayı göndersin
        fn(self.population)
       
