from record_temp_analysis import compute_max_tasmax, plot_max_tasmax_timing, get_first_last_year

# Define parameters
files_pattern = '/path/to/data/tasmax_day_reanalysis_era5_r1i1p1_{year}*.nc'
lat_range = [47.0, 55.0]  # Latitude range for the region of interest
lon_range = [5.5, 15.5]  # Longitude range for the region of interest
lat_name = 'lat'         # Name of latitude variable
lon_name = 'lon'         # Name of longitude variable

# Automatically determine the first and last year in the data
start_year, end_year = get_first_last_year(files_pattern)

# Compute the maximum tasmax and the timing over the period
max_tasmax, max_year, lats, lons = compute_max_tasmax(files_pattern, start_year, end_year, lat_range, lon_range, lat_name, lon_name)

# Plot the timing of the maximum values with specified lat and lon range
plot_max_tasmax_timing(max_year, lats, lons, lat_range, lon_range, start_year, end_year)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
