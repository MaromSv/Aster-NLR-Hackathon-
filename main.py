import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import os
from astropy import units as u
from astropy.coordinates import SkyCoord
import traceback
from dataclasses import make_dataclass

from data import get_star_data_df


stars = get_star_data_df()

plt.figure(figsize=(10, 6))
ax = plt.subplot(111, projection='aitoff')
ax.grid(True)

# Using seaborn scatterplot
sc = ax.scatter(x=stars['coord_ra_deg'], y=stars['coord_dec_deg'], c=stars['g_coord_b_rad'], cmap='viridis', s=10, alpha=0.7)


plt.title('Visible Stars', verticalalignment='bottom')
plt.show()