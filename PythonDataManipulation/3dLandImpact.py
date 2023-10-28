# -*- coding: utf-8.
"""
Created on Wed Oct 25 12:07:43 2023
@author: Sanchez-Cisneros
"""

import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rasterio

def create_crater(data, x_center, y_center, radius, max_depth):
    x, y = np.indices(data.shape)
    distance = np.sqrt((x - y_center)**2 + (y - x_center)**2)
    mask = distance < radius
    reduction_factor = max_depth * (1 - distance/radius)
    data = np.where(mask, np.maximum(data - reduction_factor, 0), data)
    return data

# Define bounding box for a small area in New Mexico
west, south, east, north = -109.05, 31.33, -103.00, 37.00

# Add your API key here
API_KEY = '04798bccdf22658bb5ae2fc00df50c73'

url = f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&west={west}&south={south}&east={east}&north={north}&outputFormat=GTiff&API_Key={API_KEY}"

response = requests.get(url)

if response.status_code == 200 and 'error' not in response.content.decode('utf-8', errors='ignore'):
    filename = "elevation_data.tif"
    with open(filename, "wb") as f:
        f.write(response.content)
    
    with rasterio.open(filename) as src:
        elevation_data = src.read(1)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(west, east, elevation_data.shape[1])
    y = np.linspace(south, north, elevation_data.shape[0])
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, elevation_data, cmap='terrain')
    ax.set_ylim(north, south)  # Inverting the Y-axis
    plt.title("Original Elevation Data")
    plt.show()

    x_center = elevation_data.shape[1] // 2
    y_center = elevation_data.shape[0] // 2
    
    # Entire region affected, so radius is set to half of data's shape
    crater_radius_grid = max(elevation_data.shape) // 2
    max_crater_depth = np.max(elevation_data)  # Maximum depth is the maximum elevation to "flatten" the area

    elevation_data_with_crater = create_crater(elevation_data.copy(), x_center, y_center, crater_radius_grid, max_crater_depth)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.plot_surface(X, Y, elevation_data_with_crater, cmap='terrain')
    ax2.set_ylim(north, south)  # Inverting the Y-axis
    plt.title("Elevation Data with Simulated Asteroid Impact")
    plt.show()

else:
    print(f"Failed to fetch the elevation data. Status Code: {response.status_code}. Response: {response.content.decode('utf-8')}")