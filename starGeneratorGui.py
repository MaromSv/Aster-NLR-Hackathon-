import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stardata import StarData


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

        self.root.update()
        data = StarData()
        data.elev = self.elevation
        data.az = self.azimuth
        result_df, visible = data.get_visible()
        fig = data.get_plot(result_df, visible)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.02, rely=0.025)
        self.root.update()
        self.root.mainloop()

    def elevationChange(self, value):
        self.elevation = value
        self.labelElevationValue.configure(text=str(int(value)))
        self.root.update()

    def azimuthChange(self, value):
        self.azimuth = value
        self.labelAzimuthValue.configure(text=str(int(value)))
        self.root.update()
