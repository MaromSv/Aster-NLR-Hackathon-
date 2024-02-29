from data import get_star_data_df
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()


def get_values(coord):
    return [coord.cartesian.x, coord.cartesian.y, coord.cartesian.z, 1]


class StarData:
    def __init__(self):
        stars = get_star_data_df()

        series = stars.coord.apply(get_values)
        self.positions = np.array(series.tolist())

    def draw_canvas(self):
        near = 0.1
        far = 1
        fov = 90
        aspect = 1

        S = 1 / np.tan(np.deg2rad(fov/2))
        b = (far+near) / (near - far)
        c = (2*far*near) / (near - far)

        projection = np.array([
            [S, 0, 0, 0],
            [0, S/aspect, 0, 0],
            [0, 0, b, c],
            [0, 0, -1, 0],
        ])

        rot_y = np.deg2rad(45)
        cos_y = np.cos(rot_y)
        sin_y = np.sin(rot_y)

        rot_x = np.deg2rad(93)
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
        visible = result_df[in_frame]

        plt.figure(figsize=(10, 6))
        ax = plt.subplot(111, projection='aitoff')
        ax.grid(True)

        # Using seaborn scatterplot
        sc = ax.scatter(x=visible['x'], y=visible['y'],
                        c="yellow", s=10, alpha=0.7)
        plt.show()



# star_data = StarData()

# star_data.draw_canvas()