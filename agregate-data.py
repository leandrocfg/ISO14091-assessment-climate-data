# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 19:49:21 2024

@author: leand
"""

import os
import pandas as pd

# Define the main folder path
main_folder = 'C://Users//leand//Downloads//Dados-Climaticos//Raw_Data'
processed_data_folder = os.path.join('C://Users//leand//Downloads//Dados-Climaticos', 'Compiled_data_with_historical')

# Function to read and process historical data
def read_and_process_historical_data(model_folder, output_variable_folder):
    historical_data = []
    historical_folder_path = os.path.join(main_folder, model_folder, output_variable_folder)
    print(f"Looking for historical data in folder: {historical_folder_path}")
    for file_name in os.listdir(historical_folder_path):
        if "Histórico_Média" in file_name:
            file_path = os.path.join(historical_folder_path, file_name)
            df = pd.read_csv(file_path, sep=';', skiprows=[0], names=["DateTime", "value"], dayfirst=True)
            df['value'] = df['value'].astype(str).str.replace('.', '').str.replace(',', '.')
            df['year'] = pd.to_datetime(df['DateTime'], dayfirst=True).dt.year
            df = df.groupby('year')['value'].sum().reset_index()
            historical_data.append(df)
    return historical_data  # Return historical data

# Iterate through the model folders
for model_folder in os.listdir(main_folder):
    if model_folder in ['BESM', 'CANESM2', 'HADGEM2-ES', 'MIROC5']:
        model_path = os.path.join(main_folder, model_folder)
        # Iterate through the output variable folders
        for output_variable_folder in os.listdir(model_path):
            output_variable_path = os.path.join(model_path, output_variable_folder)
            # Read and process historical data
            historical_data = read_and_process_historical_data(model_folder, output_variable_folder)
            
            # Initialize lists to store data
            media_rcp45_data = []
            media_rcp85_data = []
            # Iterate through the files in the output variable folder
            for file_name in os.listdir(output_variable_path):
                file_path = os.path.join(output_variable_path, file_name)
                # Exclude files containing "Histórico" or "Anomalia" in their names
                if "Histórico" not in file_name and "Anomalia" not in file_name:
                    # Read data from CSV files
                    df = pd.read_csv(file_path, sep=';', skiprows=[0], names=["DateTime", "value"], dayfirst=True)
                    df['value'] = df['value'].astype(str).str.replace('.', '').str.replace(',', '.')
                    if "Média" in file_name:
                        if "RCP4.5" in file_name:
                            media_rcp45_data.append(df[['DateTime', 'value']])  # Selecting only necessary columns
                        elif "RCP8.5" in file_name:
                            media_rcp85_data.append(df[['DateTime', 'value']])  # Selecting only necessary columns

            # Concatenate historical data with Média files
            for data, scenario, data_type in [(media_rcp45_data, "RCP4.5", "Média"),
                                              (media_rcp85_data, "RCP8.5", "Média")]:
                if data:
                    # Select relevant columns from historical data
                    historical_data_selected = [df[['year', 'value']] for df in historical_data]
                    
                    df_concat = pd.concat([*historical_data_selected, *data], ignore_index=True)
                    df_concat['year'] = pd.to_datetime(df_concat['DateTime'], dayfirst=True).dt.year
                    
                    # Group by year and sum values
                    df_concat = df_concat.groupby('year')['value'].sum().reset_index()
                    
                    # Save to CSV file
                    output_folder = os.path.join(processed_data_folder, model_folder, output_variable_folder)
                    os.makedirs(output_folder, exist_ok=True)
                    output_file_path = os.path.join(output_folder, f'Eta_{model_folder}_{output_variable_folder}_{scenario}_{data_type}_2011-2100.csv')
                    df_concat.to_csv(output_file_path, index=False, sep=';')
                    print(f"Created file: {output_file_path}")
