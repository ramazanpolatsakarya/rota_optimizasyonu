import folium.plugins
from base.data import Data


import folium
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal as Signal


class BaseTSP(QObject):
    data = None
    route_size = -1

    def __init__(self,data_path):
        super().__init__()

        self.data = Data(data_path)
        self.route_size = len(self.data.dataset)


    def draw_locations(self):
        lat_mean = np.mean(self.data.dataset["Latitude"])
        lon_mean = np.mean(self.data.dataset["Longitude"])

        coordinate = (lat_mean, lon_mean)
        m = folium.Map(tiles="Stamen Terrain", zoom_start=13, location=coordinate, attr="Stamen Design")

        sw = self.data.dataset[["Latitude", "Longitude"]].min().values.tolist()
        ne = self.data.dataset[["Latitude", "Longitude"]].max().values.tolist()

        m.fit_bounds([sw, ne])

        # Draw locations
        for i in range(len(self.data.dataset)):
            lat = self.data.dataset.at[i, "Latitude"]
            lon = self.data.dataset.at[i, "Longitude"]
            name = self.data.dataset.at[i, "Name"]
            folium.CircleMarker(
                [lat, lon],
                radius=2,
                popup=f"<div width=50px><b>{name}</b><br />lat:{lat}<br />lon:{lon}<div />",
                fill=True,
                color="purple",
            ).add_to(m)

        return m
    def draw_route(self, sequence  ):
        # sequence = route.sequence

        lat_mean = np.mean(self.data.dataset["Latitude"])
        lon_mean = np.mean(self.data.dataset["Longitude"])

        coordinate = (lat_mean, lon_mean)
        
        m = folium.Map(location=coordinate)

        sw = self.data.dataset[["Latitude", "Longitude"]].min().values.tolist()
        ne = self.data.dataset[["Latitude", "Longitude"]].max().values.tolist()

        m.fit_bounds([sw, ne])

        polyline_location_list = []

        for i in sequence:
            polyline_location_list.append(
                [
                    self.data.dataset.at[i - 1, "Latitude"],
                    self.data.dataset.at[i - 1, "Longitude"],
                ]
            )

    
        #geri dönüşü de ekliyor..
        # polyline_location_list.append(
        #     [
        #         self.data.dataset.at[sequence[0] - 1, "Latitude"],
        #         self.data.dataset.at[sequence[0] - 1, "Longitude"],
        #     ]
        # )

        # folium.PolyLine(locations=polyline_location_list, line_opacity=0.5).add_to(m)
        
        
        # Draw locations
        
        j = 0
        for i in sequence:
            j = j + 1
            
            lat = self.data.dataset.at[i-1, "Latitude"]
            lon = self.data.dataset.at[i-1, "Longitude"]
            name = self.data.dataset.at[i-1, "Name"]
            folium.CircleMarker(
                [lat, lon],
                radius=4,
                popup=f"<div width=50px><b>{name}</b><br />lat:{lat}<br />lon:{lon}<div />",
                fill=True,
                color="purple",
            ).add_to(m)
            
            if i != sequence[-1]: # son kayıt degil ise
                k = sequence[j] -1 
                lat2 = self.data.dataset.at[k, "Latitude"]
                lon2 = self.data.dataset.at[k, "Longitude"]
                listlanlon = [[lat, lon],[lat2, lon2]]

                line= folium.PolyLine(listlanlon, 
                                      line_opacity=0.5,
                                    #   color="#8EE9FF"
                                    )
                attr = {
                    # 'fill': '#007DEF', 
                    'font-weight': 'bold', 
                    'font-size': '12'}
                textpath =folium.plugins.PolyLineTextPath(line,
                                            f"({j})-{name}",
                                            center=True,
                                            offset=7,
                                            attributes=attr)
            
                m.add_child(line)
                m.add_child(textpath)

        return m
  