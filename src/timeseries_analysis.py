import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define paths to RF files
rf_files = [
    "C:/Radiative forcing/output/RF_Matrix_1980_1991.npy",
    "C:/Radiative forcing/output/RF_Matrix_1992_2000.npy",
    "C:/Radiative forcing/output/RF_Matrix_2001_2010.npy",
    "C:/Radiative forcing/output/RF_Matrix_2011_2024.npy"
]

# Step 2: Load and reshape each file to [lat, lon, time]
rf_list = []
for f in rf_files:
    data = np.load(f)  # shape: [lat, lon, 12, years]
    lat, lon, months, years = data.shape
    reshaped = data.reshape(lat, lon, months * years, order='F')  # column-major to get time in correct order
    rf_list.append(reshaped)

# Step 3: Concatenate along the time dimension
rf_data = np.concatenate(rf_list, axis=2)  # Final shape: [lat, lon, time]
print("✅ Final RF shape:", rf_data.shape)

# Step 4: Spatial average (mean over lat and lon)
rf_timeseries = np.nanmean(rf_data, axis=(0, 1))  # shape: [time]

# Step 5: Time axis for plotting
n_months = rf_timeseries.shape[0]
start_year = 1980
years_full = np.arange(start_year + (1/24), start_year + n_months / 12 + (1/24), 1/12)

# Step 6: Plotting
plt.figure(figsize=(14, 6))
plt.plot(years_full, rf_timeseries, color='blue', linewidth=1.5, label='Avg Radiative Forcing')
plt.axvline(1991 + 6/12, color='red', linestyle='--', linewidth=1.5, label='Mt. Pinatubo (1991)')
plt.title("Average trend over the Indian Subcontinent over the last four decades (1980–2024)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Radiative Forcing (W/m²)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# 🔽 Save BEFORE showing the plot
output_path = "C:/Radiative forcing/output/RF_Timeseries_1980_2024.png"
plt.savefig(output_path, dpi=300)
print(f"✅ Plot saved at: {output_path}")

# 👇 Show the plot after saving
plt.show()

