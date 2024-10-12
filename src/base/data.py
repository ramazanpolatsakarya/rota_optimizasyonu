import numpy as np
import pandas as pd
from haversine import haversine


class Data:
    dataset = None
    distance_matrix = None  # Get distances
    location_names = []

    def __init__(self, data_path):
        self.__set_data(data_path)
        self.__set_distance_matrix()

    def __set_data(self, data_path):
        if data_path[data_path.find('.'):] == ".xlsx" or data_path[data_path.find('.'):] == ".xls":            
            print("reading excel file")
            self.dataset = pd.read_excel(data_path)
        elif data_path[data_path.find('.'):] == ".csv":
            print("reading csv file")
            self.dataset = pd.read_csv(data_path, delimiter=';' ,encoding='utf-8', decimal=',')


        print(self.dataset)
                
        self.location_names = self.dataset.Name.to_list()

    def __set_distance_matrix(self):
        n = len(self.location_names)  # Number of locations
        self.distance_matrix = np.zeros((n, n))

        for i in range(0, n):
            for j in range(0, i):
                if i != j:
                    self.distance_matrix[i, j] = haversine(
                        (
                           float(self.dataset.loc[i, "Latitude"]),
                            float(self.dataset.loc[i, "Longitude"]),
                        ),
                        (
                           float( self.dataset.loc[j, "Latitude"]),
                         float(   self.dataset.loc[j, "Longitude"]),
                        ),
                    )
                    self.distance_matrix[j][i] = self.distance_matrix[i][j]