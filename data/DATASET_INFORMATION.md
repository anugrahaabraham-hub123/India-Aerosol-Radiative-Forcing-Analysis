# Dataset Information

## Dataset

This project uses the NASA MERRA-2 (Modern-Era Retrospective Analysis for Research and Applications, Version 2) atmospheric reanalysis dataset, produced by NASA's Global Modeling and Assimilation Office (GMAO). MERRA-2 provides high-resolution atmospheric datasets that are widely used for climate research. 

## Data Source

NASA GES DISC (Global Earth Sciences Data and Information Services Center)

https://disc.gsfc.nasa.gov/

NASA’s Giovanni platform

https://giovanni.gsfc.nasa.gov/giovanni/

## Study Region

Indian Subcontinent

Latitude: 0°N – 40°N

Longitude: 40°E – 100°E

## Study Period

January 1980 – December 2024

## Variables Used

### Surface of Atmosphere (SOA) Flux Variables

- **SWGNTCLR** – Surface net downward shortwave flux under clear-sky conditions.
- **SWGNTCLRCLN** – Surface net downward shortwave flux under clear-sky conditions with aerosols removed.
- **LWGNTCLR** – Surface net downward longwave flux under clear-sky conditions.
- **LWGNTCLRCLN** – Surface net downward longwave flux under clear-sky conditions with aerosols removed.

### Top of Atmosphere (TOA) Flux Variables

- **SWTNTCLR** – Net downward shortwave flux at the Top of Atmosphere (TOA) under clear-sky conditions.
- **SWTNTCLRCLN** – Net downward shortwave flux at the Top of Atmosphere (TOA) under clear-sky conditions with aerosols removed.
- **LWTUPCLR** – Upwelling longwave flux at the Top of Atmosphere (TOA) under clear-sky conditions.
- **LWTUPCLRCLN** – Upwelling longwave flux at the Top of Atmosphere (TOA) under clear-sky conditions with aerosols removed.

## Radiative Forcing Equations
SOA = (SWGNTCLR + LWGNTCLR) − (SWGNTCLRCLN + LWGNTCLRCLN)

TOA = (SWTNTCLR + LWTUPCLR) − (SWTNTCLRCLN + LWTUPCLRCLN)

ATM = TOA − SOA


These irradiance variables were used to estimate radiative forcing at the surface of the atmosphere (SOA), top of the atmosphere (TOA), and atmospheric layer (ATM).

These variables were used to calculate Aerosol Radiative Forcing (ARF).

## Data Format

- NetCDF (.nc)
- NumPy (.npy)

## Note

The original MERRA-2 datasets are not included in this repository because of their large size. Users can download the datasets from NASA GES DISC's Giovanni Platform and reproduce the analysis using the Python scripts provided in this repository.
