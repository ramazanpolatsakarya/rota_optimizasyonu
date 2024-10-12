import time

from base.BaseTSP import BaseTSP
from sa.population import PopulationSA
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


class SA_TSP(BaseTSP):
    population = None
    pop_size = -1
    number_of_children = -1
    max_generation = 0
    current_generation = -1
    parent_list = []

    result = Signal(PopulationSA)

    def __init__(self,data_path):
        
        super().__init__(data_path)
        

    def set_problem(
        self, pop_size, number_of_children, max_generation,  start,stop, T, T_min, alpha
    ):
        self.pop_size = pop_size
        self.number_of_children = number_of_children
        self.max_generation = max_generation
        self.route_size = len(self.data.dataset)
        self.start = start
        self.stop = stop
        self.current_generation = 0

        self.population = PopulationSA(
            self.max_generation,
            self.pop_size,
            self.route_size,
            self.number_of_children,
            self.data.distance_matrix,
            self.start,
            self.stop,
            T,
            T_min,
            alpha
        )

    def start_sa_thread(self):
        # print(f"progress_callback = {progress_callback}")
        
        self.population.simulated_annealing()
        
        #işlem sonunda rotayı göndersin
        self.result.emit(self.population)
       
    def start_sa(self, fn):
        # print(f"progress_callback = {progress_callback}")
        
        self.population.simulated_annealing()
        
        #işlem sonunda rotayı göndersin
        fn(self.population)
       
