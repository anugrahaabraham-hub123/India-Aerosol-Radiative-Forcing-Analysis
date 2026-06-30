import os
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Directories and file paths
matrix_files = [
    "C:/Radiative forcing/output/RF_Matrix_1980_1991.npy",
    "C:/Radiative forcing/output/RF_Matrix_1992_2000.npy",
    "C:/Radiative forcing/output/RF_Matrix_2001_2010.npy",
    "C:/Radiative forcing/output/RF_Matrix_2011_2024.npy",
]

# Output directory for plots
output_dir = "C:/Radiative forcing/plots/"
os.makedirs(output_dir, exist_ok=True)

# Metadata
lat_min, lat_max = 0, 40  # Latitude range for the Indian region
lon_min, lon_max = 40, 100  # Longitude range for the Indian region
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Helper function to process NetCDF files
def process_netcdf(file_path):
    try:
        dataset = nc.Dataset(file_path)
        print(f"Processing NetCDF file: {file_path}")

        # Extract variables
        latitude = dataset.variables['lat'][:]
        longitude = dataset.variables['lon'][:]

        # Select a variable for RF computation
        try:
            swgntclr = dataset.variables['SWGNTCLR'][:]
            lwgntclr = dataset.variables['LWGNTCLR'][:]
            lwgntclrcln = dataset.variables['LWGNTCLRCLN'][:]
            swgntclrcln = dataset.variables['SWGNTCLRCLN'][:]
            ARF_SUR = (swgntclr + lwgntclr) - (lwgntclrcln + swgntclrcln)
        except KeyError as e:
            print(f"Variable missing in NetCDF file {file_path}: {e}")
            return None, None, None, None

        # Extract date from file name
        date_str = os.path.basename(file_path).split(".")[2]
        year, month = int(date_str[:4]), int(date_str[4:6])

        # Find indices for the region
        lat_indices = np.where((latitude >= lat_min) & (latitude <= lat_max))[0]
        lon_indices = np.where((longitude >= lon_min) & (longitude <= lon_max))[0]

        # Subset data for the region
        latitude_region = latitude[lat_indices]
        longitude_region = longitude[lon_indices]
        specific_rf = ARF_SUR[0, lat_indices, :][:, lon_indices]

        return latitude_region, longitude_region, specific_rf, (year, month)
    except Exception as e:
        print(f"Error processing NetCDF file {file_path}: {e}")
        return None, None, None, None

# Iterate through all files
for file_path in matrix_files:
    if file_path.endswith(".npy"):
        # Process .npy files
        filename = os.path.basename(file_path)
        try:
            year_range = filename.replace(".npy", "").split("_")[-2:]
            start_year, end_year = map(int, year_range)
        except ValueError:
            print(f"Error: Could not extract year range from file name '{filename}'.")
            continue

        # Load the RF matrix
        try:
            RF_matrix = np.load(file_path)
        except Exception as e:
            print(f"Error loading file '{filename}': {e}")
            continue

        print(f"Loaded RF matrix for years {start_year}-{end_year}, shape: {RF_matrix.shape}")

        # Generate latitude and longitude values
        latitude = np.linspace(lat_min, lat_max, RF_matrix.shape[0])
        longitude = np.linspace(lon_min, lon_max, RF_matrix.shape[1])

        # Iterate through years and months
        for year_idx, year in enumerate(range(start_year, end_year + 1)):
            for month_idx, month_name in enumerate(months):
                specific_rf = RF_matrix[:, :, month_idx, year_idx]

                # Plot the RF data
                plt.figure(figsize=(12, 8))
                ax = plt.axes(projection=ccrs.PlateCarree())
                ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
                ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle='-', edgecolor='red')
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='black')
                ax.add_feature(cfeature.LAND, color='lightgrey')
                ax.add_feature(cfeature.OCEAN, color='lightblue')

                # Add gridlines, ticks, and labels
                gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--', linewidth=0.5)
                gl.top_labels = False
                gl.right_labels = False
                gl.xlabel_style = {'size': 10, 'color': 'black'}
                gl.ylabel_style = {'size': 10, 'color': 'black'}

                # Plot RF values
                mesh = ax.pcolormesh(
                    longitude, latitude, specific_rf,
                    transform=ccrs.PlateCarree(),
                    cmap='coolwarm',
                    vmin=-10, vmax=20
                )
                plt.colorbar(mesh, label="Radiative Forcing (RF) [W/m²]", orientation="vertical")
                plt.title(f"Radiative Forcing (RF) for {month_name} {year}")

                # Save the plot
                plot_filename = f"{output_dir}{month_name}_{year}.png"
                plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
                plt.close()
                print(f"Saved plot: {plot_filename}")

    elif file_path.endswith(".nc"):
        # Process .nc files
        latitude, longitude, specific_rf, date_info = process_netcdf(file_path)
        if specific_rf is None:
            continue

        year, month = date_info
        month_name = months[month - 1]

        # Plot the RF data
        plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle='-', edgecolor='red')
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='black')
        ax.add_feature(cfeature.LAND, color='lightgrey')
        ax.add_feature(cfeature.OCEAN, color='lightblue')

        # Add gridlines, ticks, and labels
        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--', linewidth=0.5)
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 10, 'color': 'black'}
        gl.ylabel_style = {'size': 10, 'color': 'black'}

        # Plot RF values
        mesh = ax.pcolormesh(
            longitude, latitude, specific_rf,
            transform=ccrs.PlateCarree(),
            cmap='coolwarm',
            vmin=-10, vmax=20
        )
        plt.colorbar(mesh, label="Radiative Forcing (RF) [W/m²]", orientation="vertical")
        plt.title(f"Radiative Forcing (RF) for {month_name} {year}")

        # Save the plot
        plot_filename = f"{output_dir}{month_name}_{year}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved plot: {plot_filename}")
