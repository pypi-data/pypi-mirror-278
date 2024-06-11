import numpy as np
import glob
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from tqdm import tqdm
import os

def load_yearly_data(files_pattern, year, lat_range, lon_range, lat_name, lon_name):
    files = sorted(glob.glob(files_pattern.format(year=year)))
    tasmax_list = []
    time_list = []
    lats = None
    lons = None

    for file in files:
        dataset = Dataset(file)
        if lats is None or lons is None:
            lats = dataset.variables[lat_name][:]
            lons = dataset.variables[lon_name][:]
            lat_indices = np.where((lats >= lat_range[0]) & (lats <= lat_range[1]))[0]
            lon_indices = np.where((lons >= lon_range[0]) & (lons <= lon_range[1]))[0]
            lats = lats[lat_indices]
            lons = lons[lon_indices]

        tasmax_list.append(dataset.variables['tasmax'][:, lat_indices, lon_indices])
        time = num2date(dataset.variables['time'][:], units=dataset.variables['time'].units)
        time_list.extend(time)
        dataset.close()

    tasmax = np.concatenate(tasmax_list, axis=0)
    time = np.array(time_list)
    return tasmax, time, lats, lons

def compute_max_tasmax(files_pattern, start_year, end_year, lat_range, lon_range, lat_name, lon_name):
    max_tasmax = None
    max_year = None
    lats = None
    lons = None

    for year in tqdm(range(start_year, end_year + 1), desc="Processing years"):
        tasmax, time, lats, lons = load_yearly_data(files_pattern, year, lat_range, lon_range, lat_name, lon_name)
        if max_tasmax is None:
            max_tasmax = np.max(tasmax, axis=0)
            max_year = np.full_like(max_tasmax, year, dtype=np.int32)
        else:
            current_max_tasmax = np.max(tasmax, axis=0)
            mask = current_max_tasmax > max_tasmax
            max_tasmax[mask] = current_max_tasmax[mask]
            max_year[mask] = year

    return max_tasmax, max_year, lats, lons

def plot_max_tasmax_timing(max_year, lats, lons, lat_range, lon_range, start_year, end_year):
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Set the extent to the specified latitude and longitude range
    ax.set_extent([lon_range[0], lon_range[1], lat_range[0], lat_range[1]], crs=ccrs.PlateCarree())

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)

    # Plot the timing of the maximum values using pcolor
    cmap = plt.get_cmap('RdYlBu_r')  # Reverse colormap for better representation
    norm = plt.Normalize(start_year, end_year)
    mesh = ax.pcolor(lons, lats, max_year, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.05, aspect=50, shrink=0.7)
    cbar.set_label('Year of Maximum Daily Maximum Temperature')
    cbar.set_ticks(np.arange(start_year, end_year+1, 10))
    plt.title(f'Timing of Maximum Daily Maximum Temperature from {start_year} to {end_year}')
    plt.show()

def get_first_last_year(files_pattern):
    files = glob.glob(files_pattern.format(year='*'))
    years = sorted(set(int(os.path.basename(file).split('_')[-1][:4]) for file in files))
    return min(years), max(years)


