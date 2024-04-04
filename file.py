import requests
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

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

def add_growth_column(file_path):
    """
    Add a 'growth' column to the CSV or XLSX file based on specified calculations by unique ID.
    
    Args:
    file_path (str): Path to the CSV or XLSX file.
    """
    try:
        # Determine file type
        if file_path.endswith('.csv'):
            # Read CSV file into a DataFrame
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            # Read Excel file into a DataFrame
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please provide either CSV or XLSX file.")
            return
        
        # Sort DataFrame by ID and date
        df.sort_values(by=['id', 'date'], inplace=True)
        
        # Calculate growth column by unique ID
        df['growth'] = df.groupby('id', group_keys=False)['count'].apply(lambda x: np.log(x) - np.log(x.shift(1)))
        
        # Fill NaN for growth column where ID changes
        df['growth'] = np.where(df['id'] != df['id'].shift(1), np.nan, df['growth'])
        
        # Save DataFrame back to CSV or XLSX file
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            df.to_excel(file_path, index=False)
        
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

def plot_growth_histogram(file_path, save_path):
    """
    Plot the 'growth' column from the CSV or XLSX file as a histogram,
    skipping rows containing 'n/a' or 'inf' values, and plot the normal distribution curve on top.
    
    Args:
    file_path (str): Path to the CSV or XLSX file.
    save_path (str): Path to save the plotted histogram image.
    """
    try:
        # Determine file type
        if file_path.endswith('.csv'):
            # Read CSV file into a DataFrame
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            # Read Excel file into a DataFrame
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please provide either CSV or XLSX file.")
            return
        
        # Convert 'growth' column to numeric, ignoring errors
        df['growth'] = pd.to_numeric(df['growth'], errors='coerce')
        
        # Remove rows with NaN or inf values in 'growth' column
        df = df[~df['growth'].isin([float('nan'), float('inf'), float('-inf')])]
        
        # Plot histogram
        plt.hist(df['growth'], bins=50, density=True, edgecolor='black', alpha=0.7, label='Histogram')
        
        # Calculate mean and standard deviation for the normal distribution curve
        mean, std_dev = np.mean(df['growth']), np.std(df['growth'])
        
        # Generate values for the normal distribution curve
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mean, std_dev)
        
        # Plot normal distribution curve
        plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution')
        
        plt.xlabel('Growth')
        plt.ylabel('Density')
        plt.title('Histogram of Growth with Normal Distribution')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.show()  
        
        print("Histogram with Normal Distribution plotted successfully.")
    except Exception as e:
        print("An error occurred:", e)

def reformat_excel(input_path, output_path):
    """
    Reformat the Excel file to three columns: id, date, and count, 
    including all non-empty cells from the original Excel file.
    
    Args:
    input_path (str): Path to the input Excel file.
    output_path (str): Path to save the reformatted Excel file.
    """
    try:
        # Read Excel file into a DataFrame skipping headers
        df = pd.read_excel(input_path, header=8)
        
        # Remove footer
        df = df.iloc[:-4]

        # Reset index
        df.reset_index(drop=True, inplace=True)

        # Extract dates from the "Time" column
        dates = df.iloc[:, 0]
        
        # Create an empty DataFrame for the reformatted data
        reformatted_df = pd.DataFrame(columns=['id', 'date', 'count'])
        
        # Iterate over each column in the original DataFrame
        for col in df.columns[1:]:
            # Extract non-empty cells along with their respective date and add to the reformatted DataFrame
            non_empty_cells = df.loc[df[col].notnull(), ['Time', col]]
            non_empty_cells.columns = ['date', 'count']
            non_empty_cells['id'] = col
            reformatted_df = pd.concat([reformatted_df, non_empty_cells], ignore_index=True)
        
        # Reorder columns
        reformatted_df = reformatted_df[['id', 'date', 'count']]
        
        # Save DataFrame to new Excel file
        reformatted_df.to_excel(output_path, index=False)
        
        print("Excel file reformatted successfully. Reformatted Excel saved to:", output_path)
    except Exception as e:
        print("An error occurred:", e)

def reformat_excel_dates_as_row(input_path, output_path):
    """
    Reformat the Excel file to three columns: id, date, and count, 
    including all non-empty cells from the original Excel file.
    
    Args:
    input_path (str): Path to the input Excel file.
    output_path (str): Path to save the reformatted Excel file.
    """
    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(input_path, header=8)  # Adjust header according to your file
        
        # Remove footer
        df = df.iloc[:-4]
        
        # Create an empty DataFrame for the reformatted data
        reformatted_df = pd.DataFrame(columns=['id', 'date', 'count'])
        
        # Iterate over each row in the original DataFrame
        for idx, row in df.iterrows():
            id_value = row[df.columns[0]]  # Extract id from the first column of the row
            for col in df.columns[2:]:  # Iterate over date and count columns
                year = col.split(", ")[-1]  # Extract date from column name
                value = row[col]  # Get the value in the cell
                if pd.notnull(value):  # If value is not null, add to reformatted DataFrame
                    reformatted_df = reformatted_df.append({'id': id_value, 'date': year, 'count': value}, ignore_index=True)
        
        # Convert 'date' column to integer for sorting
        reformatted_df['date'] = reformatted_df['date'].astype(int)
        
        # Sort by 'id' and 'date'
        reformatted_df = reformatted_df.sort_values(by=['id', 'date'])
        
        # Save DataFrame to new Excel file
        reformatted_df.to_excel(output_path, index=False)
        
        print("Excel file reformatted successfully. Reformatted Excel saved to:", output_path)
    except Exception as e:
        print("An error occurred:", e)

def reformat_excel_dates_as_row_strip_year(input_path, output_path):
    """
    Reformat the Excel file to three columns: id, date, and count, 
    including all non-empty cells from the original Excel file.
    
    Args:
    input_path (str): Path to the input Excel file.
    output_path (str): Path to save the reformatted Excel file.
    """
    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(input_path, header=8)  # Adjust header according to your file
        
        # Remove footer
        df = df.iloc[:-4]
        
        # Create an empty DataFrame for the reformatted data
        reformatted_df = pd.DataFrame(columns=['id', 'date', 'count'])
        
        # Iterate over each row in the original DataFrame
        for idx, row in df.iterrows():
            id_value = row[df.columns[0]]  # Extract id from the first column of the row
            for col in df.columns[2:]:  # Iterate over date and count columns
                year = col.split(", ")[-1].split(" ")[0]  # Extract year from column name
                value = row[col]  # Get the value in the cell
                if pd.notnull(value):  # If value is not null, add to reformatted DataFrame
                    reformatted_df = reformatted_df.append({'id': id_value, 'date': year, 'count': value}, ignore_index=True)
        
        # Convert 'date' column to integer for sorting
        reformatted_df['date'] = reformatted_df['date'].astype(int)
        
        # Sort by 'id' and 'date'
        reformatted_df = reformatted_df.sort_values(by=['id', 'date'])
        
        # Save DataFrame to new Excel file
        reformatted_df.to_excel(output_path, index=False)
        
        print("Excel file reformatted successfully. Reformatted Excel saved to:", output_path)
    except Exception as e:
        print("An error occurred:", e)

def reformat_excel_dates_as_row_strip_year_remove_quarter(input_path, output_path):
    """
    Reformat the Excel file to three columns: id, date, and count, 
    including all non-empty cells from the original Excel file.
    
    Args:
    input_path (str): Path to the input Excel file.
    output_path (str): Path to save the reformatted Excel file.
    """
    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(input_path, header=8)  # Adjust header according to your file
        
        # Remove footer
        df = df.iloc[:-4]
        
        # Create an empty DataFrame for the reformatted data
        reformatted_df = pd.DataFrame(columns=['id', 'date', 'count'])
        
        # Iterate over each row in the original DataFrame
        for idx, row in df.iterrows():
            id_value = row[df.columns[0]]  # Extract id from the first column of the row
            for col in df.columns[2:]:  # Iterate over date and count columns
                year = col.split(", ")[-1].split(" ")[0]  # Extract year from column name
                value = row[col]  # Get the value in the cell
                if pd.notnull(value):  # If value is not null, add to reformatted DataFrame
                    reformatted_df = reformatted_df.append({'id': id_value, 'date': year, 'count': value}, ignore_index=True)
        
        # Remove '/3' from the 'date' column
        reformatted_df['date'] = reformatted_df['date'].str.split('/').str[0]
        
        # Convert 'date' column to integer for sorting
        reformatted_df['date'] = reformatted_df['date'].astype(int)
        
        # Sort by 'id' and 'date'
        reformatted_df = reformatted_df.sort_values(by=['id', 'date'])
        
        # Save DataFrame to new Excel file
        reformatted_df.to_excel(output_path, index=False)
        
        print("Excel file reformatted successfully. Reformatted Excel saved to:", output_path)
    except Exception as e:
        print("An error occurred:", e)
        
# def reformat_excel_dates_as_row_second_index(input_path, output_path):
#     """
#     Reformat the Excel file to three columns: id, date, and count, 
#     including all non-empty cells from the original Excel file.
    
#     Args:
#     input_path (str): Path to the input Excel file.
#     output_path (str): Path to save the reformatted Excel file.
#     """
#     try:
#         # Read Excel file into a DataFrame
#         df = pd.read_excel(input_path, header=8)  # Adjust header according to your file
        
#         # Remove footer
#         df = df.iloc[:-4]
        
#         # Create an empty DataFrame for the reformatted data
#         reformatted_df = pd.DataFrame(columns=['id', 'date', 'count'])
        
#         # Iterate over each row in the original DataFrame
#         for idx, row in df.iterrows():
#             id_value = row[df.columns[0]]  # Extract id from the first column of the row
#             for col in df.columns[2:]:  # Iterate over date and count columns
#                 year = col.split(", ")[-2]  # Extract date from column name
#                 value = row[col]  # Get the value in the cell
#                 if pd.notnull(value):  # If value is not null, add to reformatted DataFrame
#                     reformatted_df = reformatted_df.append({'id': id_value, 'date': year, 'count': value}, ignore_index=True)
        
#         # Convert 'date' column to integer for sorting
#         reformatted_df['date'] = reformatted_df['date'].astype(int)
        
#         # Sort by 'id' and 'date'
#         reformatted_df = reformatted_df.sort_values(by=['id', 'date'])
        
#         # Save DataFrame to new Excel file
#         reformatted_df.to_excel(output_path, index=False)
        
#         print("Excel file reformatted successfully. Reformatted Excel saved to:", output_path)
#     except Exception as e:
#         print("An error occurred:", e)

# xlsx = "total_us_troop_deployment_sage"
# original_csv_path = "original_csv" + "/" + xlsx + ".xlsx"
# modified_csv_path = "modified_csv" + "/" + xlsx + ".xlsx"
# graph_path = "graphs" + "/" + xlsx
# reformat_excel_dates_as_row_strip_year_remove_quarter(original_csv_path, modified_csv_path)
# add_growth_column(modified_csv_path)
# plot_growth_histogram(modified_csv_path, graph_path)