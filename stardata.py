from algorithm import algorithm
from data import get_star_data_df
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
import mplcursors
from mpl_interactions import ioff, panhandler, zoom_factory

pd.plotting.register_matplotlib_converters()


def get_values(coord):
    return [coord.cartesian.x, coord.cartesian.y, coord.cartesian.z, 1]


class StarData:
    def __init__(self):
        self.stars = get_star_data_df()

        series = self.stars.coord.apply(get_values)
        self.positions = np.array(series.tolist())
        self.constellations = []
        self.user_edges = []
        # put these as parameters
        self.fov = 90
        self.az = 45
        self.elev = 90

    def get_visible(self):
        near = 0.1
        far = 1
        aspect = 1

        S = 1 / np.tan(np.deg2rad(self.fov/2))
        b = (far+near) / (near - far)
        c = (2*far*near) / (near - far)

        projection = np.array([
            [S, 0, 0, 0],
            [0, S/aspect, 0, 0],
            [0, 0, b, c],
            [0, 0, -1, 0],
        ])

        rot_y = np.deg2rad(self.az)
        cos_y = np.cos(rot_y)
        sin_y = np.sin(rot_y)

        rot_x = np.deg2rad(self.elev)
        cos_x = np.cos(rot_x)
        sin_x = np.sin(rot_x)

        r_y = np.array([
            [cos_y, 0, sin_y, 0],
            [0, 1, 0, 0],
            [-sin_y, 0, cos_y, 0],
            [0, 0, 0, 1]
        ])

        r_x = np.array([
            [1, 0, 0, 0],
            [0, cos_x, -sin_x, 0],
            [0, sin_x, cos_x, 0],
            [0, 0, 0, 1]
        ])

        rotated_pos = self.positions@r_y@r_x

        result = rotated_pos@projection
        result_df = pd.DataFrame(result)

        result_df["x"] = result_df[0] / result_df[3]
        result_df["y"] = result_df[1] / result_df[3]
        result_df["z"] = result_df[2] / result_df[3]

        in_frame = ((result_df["z"] > -1) & (result_df["z"] < 1)) & ((result_df["x"] > -1)
                                                                     & (result_df["x"] < 1)) & ((result_df["y"] > -1) & (result_df["y"] < 1))

        result_df["id"] = self.stars["id"]
        result_df = result_df["x", "y", "z", "id"]
        visible = result_df[in_frame]
        return result_df, visible

    def get_plot(self, result_df, visible):

        fig = Figure(figsize=(11.5, 6.5), tight_layout=True, facecolor="black")

        ax = fig.add_subplot(111)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.tick_params(left=False, bottom=False)
        ax.set_facecolor('black')

        # Using seaborn scatterplot
        ax.scatter(x=visible['x'], y=visible['y'],
                   c="yellow", s=10, alpha=0.7, picker=True)
        for edge in self.user_edges:
            first_row = result_df[result_df["id"]
                                  == self.constellations[edge[0]]]
            second_row = result_df[result_df["id"]
                                   == self.constellations[edge[0]]]
            ax.plot([first_row["x"].iloc[0], second_row["x"].iloc[0]], [
                    first_row["y"].iloc[0], second_row["y"].iloc[0]], 'b-')

        self.crs = mplcursors.cursor(ax, hover=2)

        self.crs.connect("add", lambda sel: sel.annotation.set_text(
            'Star #{}\nx={}, y={}'.format(sel.index, sel.target[0], sel.target[1])))

        disconnect_zoom = zoom_factory(ax)
        pan_handler = panhandler(fig)
        plt.show()

        return fig

    def figureLeave(self, event):
        self.crs.visible = False

    def figureEnter(self, event):
        self.crs.visible = True
