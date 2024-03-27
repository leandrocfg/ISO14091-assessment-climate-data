import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Function to calculate linear regression slope
def calculate_slope(x, y):
    model = LinearRegression()
    model.fit(x.values.reshape(-1, 1), y)
    return model.coef_[0]

def process_files(main_folder, last_year):
    processed_data_folder = os.path.join('C://Users//leand//Downloads//Dados-Climaticos//Processed-data', f'{last_year}')
    slopes_file_path = os.path.join(processed_data_folder, f'slopes_{last_year}.csv')

    print("Processing files in:", main_folder)

    # Create processed data folder if it does not exist
    if not os.path.exists(processed_data_folder):
        os.makedirs(processed_data_folder)

    # Create an empty list to store slopes
    slopes = []

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
                
                # # Plot data and trend line
                plt.figure()
                plt.plot(df['year'], df['value'], label='Data', linestyle='-')
                plt.xlabel('Year')
                plt.ylabel({'CDD': 'Days', 'CWD': 'Days', 'R95p': 'mm', 'RX1day': 'mm', 'RX5day': 'mm',
                            'SDII': 'mm/day', 'TX90p': '%', 'W10M': 'm/s', 'UR': '%'}[output_variable])
                plt.title(f"{output_variable} {model} {scenario} {data_type}")
                
                # # Calculate linear regression slope
                slope = calculate_slope(df['year'], df['value'])
                slopes.append([output_variable, model, scenario, data_type, slope])
                
                # Plot trend line
                x_values = np.array(df['year']).reshape(-1, 1)
                y_values = np.array(df['value'])
                regression_model = LinearRegression().fit(x_values, y_values)
                plt.plot(df['year'], regression_model.predict(x_values), label='Trend line', linestyle='--')
                
                plt.legend()
                
                # Create model folder if it doesn't exist
                model_folder = os.path.join(processed_data_folder, model)
                if not os.path.exists(model_folder):
                    os.makedirs(model_folder)
                
                # # Save plot in the processed_data_folder with model name included
                plot_file_path = os.path.join(model_folder, f'{output_variable}_{model}_{scenario}_{data_type}_{last_year}_plot.png')
                plt.savefig(plot_file_path)
                plt.close()

    # # Save slopes to a CSV file
    slopes_df = pd.DataFrame(slopes, columns=['Variable', 'Model', 'Scenario', 'Data Type', 'Slope'])
    slopes_df.to_csv(slopes_file_path, index=False, encoding='utf-8')

    print("Plots and slopes saved successfully.")

# Example usage
last_year = int(input("Enter the last year for calculations: "))
main_folder = 'C://Users//leand//Downloads//Dados-Climaticos//Compiled-data'
process_files(main_folder, last_year)