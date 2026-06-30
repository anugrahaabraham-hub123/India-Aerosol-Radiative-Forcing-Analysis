import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# File paths
seasonal_rf_dir = "C:/Radiative forcing/output/seasonal/"
season_files = {
    "Winter": "RF_DJF_1981_2024.npy",
    "Pre-monsoon": "RF_MAM_1980_2024.npy",
    "Monsoon": "RF_JJA_1980_2024.npy",
    "Post-monsoon": "RF_SON_1980_2024.npy"
}

# Coordinates
lat_min, lat_max = 0, 40
lon_min, lon_max = 40, 100
nlat, nlon = 41, 61
latitudes = np.linspace(lat_min, lat_max, nlat)
longitudes = np.linspace(lon_min, lon_max, nlon)

# Output path for combined plot
output_path = "C:/Radiative forcing/plots/Seasonal_RF_Combined_Labeled.png"

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(16, 12), subplot_kw={'projection': ccrs.PlateCarree()})
fig.suptitle("Seasonal Average Radiative Forcing over India (1980–2024)", fontsize=18)

# Season order for subplot positions
season_order = ["Winter", "Pre-monsoon", "Monsoon", "Post-monsoon"]

for ax, season in zip(axes.flat, season_order):
    filepath = os.path.join(seasonal_rf_dir, season_files[season])
    rf_data = np.load(filepath)  # Shape: [lat, lon, time]
    rf_mean = np.mean(rf_data, axis=2)  # Average over time

    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle='--', edgecolor='black')
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='gray')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--', linewidth=0.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 9}
    gl.ylabel_style = {'size': 9}

    mesh = ax.pcolormesh(longitudes, latitudes, rf_mean, transform=ccrs.PlateCarree(),
                         cmap='coolwarm', vmin=-10, vmax=20)
    ax.set_title(f"{season}", fontsize=14)

# Add a single colorbar at the bottom
cbar_ax = fig.add_axes([0.25, 0.08, 0.5, 0.02])  # [left, bottom, width, height]
cbar = fig.colorbar(mesh, cax=cbar_ax, orientation='horizontal')
cbar.set_label("Radiative Forcing [W/m²]")

# Save the combined figure
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Labeled seasonal RF plot saved at: {output_path}")
