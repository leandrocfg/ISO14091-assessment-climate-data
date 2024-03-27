# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:10:49 2024

@author: leand
"""

import os
import pandas as pd
from scipy.stats import combine_pvalues

# Function to calculate combined p-value using Fisher method
def metodo_fisher(p_values_list):
    _, combined_p_value = combine_pvalues(p_values_list, method='fisher')
    return combined_p_value

# Function to determine confidence level based on p-value
def determine_confidence_level(p_value):
    if p_value < 0.01:
        return 'Very High Confidence'
    elif 0.01 <= p_value < 0.05:
        return 'High Confidence'
    elif 0.05 <= p_value < 0.1:
        return 'Medium Confidence'
    elif 0.1 <= p_value < 0.2:
        return 'Low Confidence'
    else:
        return 'Very Low Confidence'

def process_files(main_folder, last_year):
    # Read the CSV file
    Z_val_file_folder = os.path.join(main_folder, f'{last_year}')
    Z_val_file_path = os.path.join(Z_val_file_folder, f'mann_kendall_{last_year}.csv')
    df = pd.read_csv(Z_val_file_path, encoding='utf-8')
    
    # # Extract the directory path from the input file path
    # output_folder = os.path.dirname(Z_val_file_path)
    
    # Initialize a dictionary to store p-values lists for each combination of variable and data type
    p_values_dict = {}
    
    # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        key = (row['Variable'], row['Data Type'])
        if key not in p_values_dict:
            p_values_dict[key] = []
        p_values_dict[key].append(row['p-value'])
    
    # Initialize list to store combined p-values and confidence levels
    combined_p_values = []
    confidence_levels = []
    
    # Iterate over p-values lists and calculate combined p-values
    for key, p_values_list in p_values_dict.items():
        variable, data_type = key
        print(f'Variable: {variable}, Data Type: {data_type}, p_values_list: {p_values_list}')
        combined_p_value = metodo_fisher(p_values_list)
        print(f'Variable: {variable}, Data Type: {data_type}, Combined p-value: {combined_p_value}')
        confidence_level = determine_confidence_level(combined_p_value)
        combined_p_values.append([variable, data_type, combined_p_value, confidence_level])
        confidence_levels.append(confidence_level)
    
    # Write results to CSV file
    output_file_path = os.path.join(Z_val_file_folder, f'combined_p_values_{last_year}.csv')
    combined_p_values_df = pd.DataFrame(combined_p_values, columns=['Variable', 'Data Type', 'Combined p-value', 'Confidence Level'])
    combined_p_values_df.to_csv(output_file_path, index=False, encoding='utf-8')

# Example usage
last_year = int(input("Enter the last year for calculations: "))
# p_value = float(input("Enter the desired p-value for the Mann Zendall Calculation: "))
main_folder = 'C://Users//leand//Downloads//Dados-Climaticos//Processed-Data'
process_files(main_folder, last_year)