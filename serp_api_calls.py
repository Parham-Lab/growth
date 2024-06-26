# pip install google-search-results 
from serpapi import GoogleSearch
import pandas as pd
from file import add_growth_column, plot_growth_histogram
import os
import re
from datetime import datetime

def parse_date(date_string):
    # Define regex pattern to extract date and time components
    pattern = r'(\w{3} \d{2} \d{4}), (\d{2}:\d{2} [AP]M)'
    match = re.match(pattern, date_string)
    
    if match:
        date_component = match.group(1)
        time_component = match.group(2)
        datetime_string = f"{date_component}, {time_component}"
        
        # Parse datetime string into a datetime object
        return datetime.strptime(datetime_string, "%b %d %Y, %I:%M %p")
    else:
        raise ValueError("Invalid date string format")

# Create serp_files directory if it doesn't exist
if not os.path.exists('serp_files'):
    os.makedirs('serp_files')

# GOOGLE FINANCE - STOCK PRICES
ids = ["GOOGL", "NVDA", "INTC", "AMZN", "AAPL", "TSLA", "MSFT"]

# Create an empty DataFrame to store data
dfs = []

for id in ids:
    params = {
        "api_key": "ccd76c1a289a9b4d5d65f21ca3dff1937566d4154c361da419dba9fd2876ccc5",
        "engine": "google_finance",
        "q": id + ":NASDAQ",
        "window": "MAX",
        "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Check if 'graph' key exists in results and if it's not empty
    if 'graph' in results and results['graph']:
        try:
            # Create DataFrame for current ID
            df = pd.DataFrame(columns=['id', 'date', 'count'])

            # Iterate over graph data and append to DataFrame
            for data_point in results['graph']:
                df = df.append({'id': id, 'date': parse_date(data_point['date']),
                                'count': data_point['price']}, ignore_index=True)
            
            dfs.append(df)
        except Exception as e:
            print("An error occurred:", e)
    else:
        print(f"No data found for {id} in 'graph' key.")

# Concatenate all DataFrames into a single DataFrame
df = pd.concat(dfs)

# Sort DataFrame by 'id' and then by 'date'
df = df.sort_values(by=['id', 'date'])

# Save DataFrame to Excel in serp_files directory
excel_file_path = os.path.join('serp_files', 'stocks.xlsx')
df.to_excel(excel_file_path, index=False)
print("Excel workbook saved successfully.")

# Examine growth phenomena
add_growth_column(excel_file_path)
plot_growth_histogram(excel_file_path, os.path.join('serp_files', 'stocks'))

print("Plots saved successfully.")
