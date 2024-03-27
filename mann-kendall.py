# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 23:12:55 2024

@author: leand
"""

import os
import pandas as pd
import pymannkendall as mk

# Function to performe Mann Kendall test
def calculate_mann_kendall(x, y):
    # Perform the Mann-Kendall test
    mk_test_result = mk.original_test(y)

    # Extract the Z-value from the test result
    z_value = mk_test_result.z
    trend = mk_test_result.trend
    h = mk_test_result.h
    p = mk_test_result.p
    s = mk_test_result.s
    var_s = h = mk_test_result.var_s
    slope_mann = h = mk_test_result.slope
    return [trend, h, z_value, p, s, var_s, slope_mann]

def process_files(main_folder, last_year):
    processed_data_folder = os.path.join('C://Users//leand//Downloads//Dados-Climaticos//Processed-Data', f'{last_year}')
    mann_kendall_file_path = os.path.join(processed_data_folder, f'mann_kendall_{last_year}.csv')

    print("Processing files in:", main_folder)

    # Create an empty list to store mann_kendalls test data
    mann_kendalls = []

    # Iterate through the original data files
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print("Processing file:", file_path)
                # Read the CSV file
                df = pd.read_csv(file_path, sep=';')
                
                # Check if 'year' column exists
                if 'year' not in df.columns:
                    print("Warning: 'year' column not found in the DataFrame. Skipping file:", file_path)
                    continue
                
                # Filter data based on last year
                df = df[df['year'] <= last_year]
                
                # Extract information from the file path
                _, model, output_variable, scenario, data_type, _ = file.split('_')
                
                # Z-value for mann_kendall test
                results = calculate_mann_kendall(df['year'], df['value'])
                mann_kendalls.append([output_variable, model, scenario, data_type] + results)
                

    # Save Z-values for Mann-Kendall test to a CSV file
    mann_kendalls_df = pd.DataFrame(mann_kendalls, columns=['Variable', 'Model', 'Scenario', 'Data Type', 'Trend', 'h', 'Z-value', 'p-value', 's', 'var_s', 'Slope'])
    mann_kendalls_df.to_csv(mann_kendall_file_path, index=False, encoding='utf-8')

    print("Mann Kendall test done. Plots and slopes saved successfully.")

# Example usage
last_year = int(input("Enter the last year for calculations: "))
# p_value = float(input("Enter the desired p-value for the Mann Zendall Calculation: "))
main_folder = 'C://Users//leand//Downloads//Dados-Climaticos//Compiled-Data'
process_files(main_folder, last_year)