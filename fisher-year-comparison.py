# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:11:14 2024

@author: leand
"""

import os
import pandas as pd

# Define the folder path
folder_path = 'C://Users//leand//Downloads//Dados-Climaticos//Processed-Data-with-historical'

# Initialize a DataFrame to store the combined p-values and confidence levels
combined_df = pd.DataFrame()

# Initialize the first two columns
combined_df[['Variable', 'Data Type']] = None

# Read the first CSV file to get the data for the first two columns
first_csv_file = None
for folder_name in os.listdir(folder_path):
    folder_year_path = os.path.join(folder_path, folder_name)
    if os.path.isdir(folder_year_path):
        folder_year = folder_name.split('_')[-1]
        csv_file_path = os.path.join(folder_year_path, f'combined_p_values_{folder_year}.csv')
        if os.path.isfile(csv_file_path):
            first_csv_file = csv_file_path
            break

if first_csv_file:
    first_df = pd.read_csv(first_csv_file)
    combined_df[['Variable', 'Data Type']] = first_df[['Variable', 'Data Type']]

# Initialize lists to store combined p-values and confidence levels
combined_p_values = []
confidence_levels = []

# Iterate over the folders inside the main folder
for folder_name in os.listdir(folder_path):
    # Construct the folder path
    folder_year_path = os.path.join(folder_path, folder_name)
    
    # Check if the current item is a directory representing a year
    if os.path.isdir(folder_year_path):
        folder_year = folder_name.split('_')[-1]  # Extract the year from the folder name
        folder_year = int(folder_year)  # Convert year to integer
        print(folder_year)
        
        # Construct the file path for the CSV file
        csv_file_path = os.path.join(folder_year_path, f'combined_p_values_{folder_year}.csv')
        
        # Check if the CSV file exists
        if os.path.isfile(csv_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)
            
            # Append the columns to the lists
            combined_p_values.append(df['Combined p-value'])
            confidence_levels.append(df['Confidence Level'])

# Transpose the lists and concatenate them horizontally
combined_df = pd.concat([combined_df] + combined_p_values + confidence_levels, axis=1)

# Save the combined DataFrame to an Excel file
output_file_path = os.path.join(folder_path, 'combined_data.xlsx')
combined_df.to_excel(output_file_path, index=False)

print("Combined data saved successfully to:", output_file_path)