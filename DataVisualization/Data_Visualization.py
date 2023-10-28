# -*- coding: utf-8.
"""
Created on Sat Oct 28 13:48:55 2023

@author: Sanchez-Cisneros
"""

import pandas as pd
import matplotlib.pyplot as plt

# URL of the Champagne Sales dataset
DATA_URL = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv'

# Load the dataset using pandas
data = pd.read_csv(DATA_URL, delimiter=',')

# Since the dataset does not have column headers, let's assign them
data.columns = ['Month', 'Sales']

# Plotting the trend
plt.figure(figsize=(12, 7))
plt.plot(data['Month'], data['Sales'], marker='o', linestyle='-')
plt.title('Monthly Champagne Sales')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.xticks(rotation=45)  # rotate x labels for better visibility
plt.grid(True)
plt.tight_layout()
plt.show()


