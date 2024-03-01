import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stardata import StarData
from algorithm import findConstellation


class StarGenerator(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        self.elevation = 0
        self.azimuth = 0

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("Star Scribbler")
        self.root.update()

        self.labelElevation = ctk.CTkLabel(
            master=self.root, text="Elevation", font=('TkDefaultFont', 15))
        self.labelAzimuth = ctk.CTkLabel(
            master=self.root, text="Azimuth", font=('TkDefaultFont', 15))
        self.labelElevationValue = ctk.CTkLabel(
            master=self.root, text="0", font=('TkDefaultFont', 15))
        self.labelAzimuthValue = ctk.CTkLabel(
            master=self.root, text="0", font=('TkDefaultFont', 15))

        self.sliderElevation = ctk.CTkSlider(
            master=self.root, from_=-180, to=180, height=20, width=1000, command=self.elevationChange)
        self.sliderAzimuth = ctk.CTkSlider(
            master=self.root, from_=0, to=300, height=20, width=1000, command=self.azimuthChange)

        self.labelElevation.place(relx=0.02, rely=0.895)
        self.labelAzimuth.place(relx=0.02, rely=0.945)
        self.labelElevationValue.place(relx=0.95, rely=0.895)
        self.labelAzimuthValue.place(relx=0.95, rely=0.945)

        self.sliderElevation.place(relx=0.1, rely=0.9)
        self.sliderAzimuth.place(relx=0.1, rely=0.95)
        self.sliderAzimuth.set(0)

        self.starData = StarData()
        self.root.update()
        

    def plot(self, verticies, edges):
       
        #Convert to list
        vertex_lists = np.array([[vertex.x, vertex.y] for vertex in verticies])
        print(vertex_lists)
        # Convert Edge objects to lists
        edge_lists = np.array([[edge.vertex1.index, edge.vertex2.index] for edge in edges])
        print(edge_lists)
    

        #Get x and y coordinates of plotted stars
        self.starData.elev = self.elevation
        self.starData.az = self.azimuth
        result_df, visible = self.starData.get_visible()

        starx = visible['x'].tolist()
        stary = visible['y'].tolist()
        ids = visible['id'].tolist()

        #Call Algorithm
        
        final_constellation_with_ids = findConstellation(starx, stary, ids, vertex_lists, edge_lists)
      
        final_constellation = final_constellation_with_ids[0]
        final_constellation_ids = final_constellation_with_ids[2]

        self.starData.user_edges = edge_lists
        print(final_constellation_ids)
        self.starData.constellations = final_constellation_ids
        

        self.fig = self.starData.get_plot(result_df, visible)
      
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.02, rely=0.025)
        self.root.update()

    def elevationChange(self, value):
        self.elevation = value
        self.labelElevationValue.configure(text=str(int(value)))
        self.starData.elev = self.elevation
        self.starData.az = self.azimuth

        result_df, visible = self.starData.get_visible()
        self.fig = self.starData.get_plot(result_df, visible)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.02, rely=0.025)
        self.root.update()

    def azimuthChange(self, value):
        self.azimuth = value
        self.labelAzimuthValue.configure(text=str(int(value)))
        self.starData.elev = self.elevation
        self.starData.az = self.azimuth

        result_df, visible = self.starData.get_visible()
        self.fig = self.starData.get_plot(result_df, visible)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.02, rely=0.025)
        self.root.update()
