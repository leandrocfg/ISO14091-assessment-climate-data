# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 18:40:37 2024

@author: leand
"""

import os
import glob
import pandas as pd

# Define the path to the source and destination folders
source_folder = "C://Users//leand//Downloads//Dados-Climaticos//Raw_data"
destination_folder = "C://Users//leand//Downloads//Dados-Climaticos//Compiled-data-with-historical"

# Define the model names and output variables
models = ["BESM", "CANESM2", "HADGEM2-ES", "MIROC5"]
output_variables = ["CDD", "CWD", "R95p", "RX1day", "RX5day", "SDII", "TX90p", "UR", "W10M"]

# Ensure the destination directory exists
os.makedirs(destination_folder, exist_ok=True)

# Function to process and combine files including historical data
def process_and_combine_files(model, variable, scenario):
    historical_pattern = f"{source_folder}/{model}/{variable}/*Histórico_Média*.csv"
    historical_file = glob.glob(historical_pattern)
    scenario_pattern = f"{source_folder}/{model}/{variable}/*{scenario}_Média*.csv"
    scenario_files = glob.glob(scenario_pattern)

    combined_data = []

    # Read and append historical data if it exists
    if historical_file:
        historical_data = pd.read_csv(historical_file[0], delimiter=';', header=None, usecols=[0, 1], skiprows=1)
        historical_data[0] = pd.to_datetime(historical_data[0]).dt.year
        historical_data[1] = historical_data[1].astype(str).str.replace(',', '.').astype(float)
        historical_data[1] = historical_data[1].apply(lambda x: f"{x:.5f}")
        combined_data.append(historical_data)

    # Read and append scenario data
    for file in sorted(scenario_files):
        data = pd.read_csv(file, delimiter=';', header=None, usecols=[0, 1], skiprows=1)
        data[0] = pd.to_datetime(data[0]).dt.year
        data[1] = data[1].astype(str).str.replace(',', '.').astype(float)
        data[1] = data[1].apply(lambda x: f"{x:.2f}")
        combined_data.append(data)

    # Concatenate all dataframes
    combined_df = pd.concat(combined_data, ignore_index=True).sort_values(by=[0])

    # Save the combined data to a new CSV file
    output_path = os.path.join(destination_folder, model, variable)
    os.makedirs(output_path, exist_ok=True)
    combined_df.to_csv(os.path.join(output_path, f"Eta_{model}_{variable}_{scenario}_Média_1961-2100.csv"), index=False, header=["year", "value"], sep=';')

# Loop through each model and output variable
for model in models:
    for variable in output_variables:
        # Process for RCP4.5 scenario
        process_and_combine_files(model, variable, "RCP4.5")
        # Process for RCP8.5 scenario
        process_and_combine_files(model, variable, "RCP8.5")
