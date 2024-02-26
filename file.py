import requests
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# def download_file(url, save_path):
#     """
#     Download file from URL and save it to the specified path.
#     """
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(save_path, 'wb') as f:
#             f.write(response.content)
#         print("File downloaded successfully.")
#     else:
#         print("Failed to download file.")

# def open_excel_file(file_path):
#     """
#     Open Excel file using pandas.
#     """
#     try:
#         df = pd.read_excel(file_path)
#         print(df)
#     except Exception as e:
#         print("An error occurred while opening the Excel file:", e)

# def main():
#     url = input("Enter the URL of the Excel file: ")
#     file_name = url.split('/')[-1]
#     save_path = os.path.join(os.getcwd(), file_name)
    
#     download_file(url, save_path)
#     open_excel_file(save_path)

# if __name__ == "__main__":
#     main()

def rename_and_keep_columns(csv_path, columns_to_keep_and_rename, path):
    """
    Rename specified columns in a CSV file while keeping them.
    
    Args:
    csv_path (str): Path to the CSV file to read from.
    columns_to_keep_and_rename (dict): Dictionary where keys are the current column names
                                       and values are the new column names.
    path (str): Path to save the modified CSV file.
    """
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Filter DataFrame to keep only specified columns
        df = df[[col for col in df.columns if col in columns_to_keep_and_rename]]
        
        # Rename specified columns
        df.rename(columns=columns_to_keep_and_rename, inplace=True)
        
        # Save DataFrame to new CSV file
        df.to_csv(path, index=False)
        
        print("Columns renamed and kept successfully. Modified CSV saved to:", path)
    except Exception as e:
        print("An error occurred:", e)

def add_count_cleaned_column(csv_path):
    """
    Add a 'count_cleaned' column to the Excel file based on the difference between consecutive 'count' values per unique ID.
    
    Args:
    excel_path (str): Path to the Excel file.
    """
    try:
        # Read Excel file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Sort DataFrame by ID and date
        df.sort_values(by=['id', 'date'], inplace=True)
        
        # Calculate count_cleaned column by subtracting the previous count value within each group
        df['count_cleaned'] = df.groupby('id')['count'].diff()
        
        # Save DataFrame back to Excel file
        df.to_csv(csv_path, index=False)
        
        print("count_cleaned column added successfully.")
    except Exception as e:
        print("An error occurred:", e)

def add_growth_column(csv_path):
    """
    Add a 'growth' column to the CSV file based on specified calculations by unique ID.
    
    Args:
    csv_path (str): Path to the CSV file.
    """
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Sort DataFrame by ID and date
        df.sort_values(by=['id', 'date'], inplace=True)
        
        # Calculate growth column by unique ID
        df['growth'] = df.groupby('id', group_keys=False)['count'].apply(lambda x: np.log(x) - np.log(x.shift(1)))
        
        # Fill NaN for growth column where ID changes
        df['growth'] = np.where(df['id'] != df['id'].shift(1), np.nan, df['growth'])
        
        # Save DataFrame back to CSV file
        df.to_csv(csv_path, index=False)
        
        print("Growth column added successfully.")
    except Exception as e:
        print("An error occurred:", e)

def add_growth_cleaned_column(csv_path):
    """
    Add a 'growth' column to the CSV file based on specified calculations by unique ID.
    
    Args:
    csv_path (str): Path to the CSV file.
    """
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Sort DataFrame by ID and date
        df.sort_values(by=['id', 'date'], inplace=True)
        
        # Calculate growth column by unique ID
        df['growth'] = df.groupby('id', group_keys=False)['count_cleaned'].apply(lambda x: np.log(x) - np.log(x.shift(1)))
        
        # Fill NaN for growth column where ID changes
        df['growth'] = np.where(df['id'] != df['id'].shift(1), np.nan, df['growth'])
        
        # Save DataFrame back to CSV file
        df.to_csv(csv_path, index=False)
        
        print("Growth column added successfully.")
    except Exception as e:
        print("An error occurred:", e)

def plot_growth_histogram(csv_path, save_path):
    """
    Plot the 'growth' column from the CSV file as a histogram,
    skipping rows containing 'n/a' or 'inf' values.
    
    Args:
    csv_path (str): Path to the CSV file.
    """
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Convert 'growth' column to numeric, ignoring errors
        df['growth'] = pd.to_numeric(df['growth'], errors='coerce')
        
        # Remove rows with NaN or inf values in 'growth' column
        df = df[~df['growth'].isin([float('nan'), float('inf'), float('-inf')])]
        
        # Plot histogram
        plt.hist(df['growth'], bins=50, edgecolor='black')
        plt.xlabel('Growth')
        plt.ylabel('Frequency')
        plt.title('Histogram of Growth')

        plt.xlim(-2, 2)
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.show()  
        
        print("Histogram plotted successfully.")
    except Exception as e:
        print("An error occurred:", e)
