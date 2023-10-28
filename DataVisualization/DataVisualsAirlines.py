# -*- coding: utf-8.
"""
Created on Sat Oct 28 15:33:35 2023

@author: Sanchez-Cisneros
"""
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# URL of the Airline Passengers dataset
DATA_URL = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv'

# Load the dataset using pandas
data = pd.read_csv(DATA_URL)

# 1. Line plot for the trend over the years
plt.figure(figsize=(27, 7))
plt.plot(data['Month'], data['Passengers'], marker='o', linestyle='--')
plt.title('Monthly International Airline Passengers')
plt.xlabel('1949 to 1961')
plt.ylabel('Passengers')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Histogram for the distribution of monthly passengers
plt.figure(figsize=(12, 7))
plt.hist(data['Passengers'], bins=20, edgecolor='k')
plt.title('Distribution of Monthly Passengers')
plt.xlabel('Passengers')
plt.ylabel('Number of Months')
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Box plot for annual distribution
# Extracting the year from the Month column
data['Year'] = data['Month'].apply(lambda x: int(x.split('-')[0]))
grouped_data = [data[data['Year'] == year]['Passengers'].values for year in range(1949, 1961)]
plt.figure(figsize=(12, 7))
plt.boxplot(grouped_data, patch_artist=True, vert=True)
plt.title('Annual Distribution of Passengers')
plt.xlabel('Year')
plt.ylabel('Passengers')
plt.xticks(ticks=range(1, 13), labels=range(1949, 1961))
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
