import requests
# pip install bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from file import add_growth_column, plot_growth_histogram
import os

def extract_names_from_page(page_url):
    # get URL
    page = requests.get(page_url)
     
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
     
    # find all td tags with a link and a title attribute
    td_with_links = soup.find_all('td', {'class': None, 'align': None, 'rowspan': None}) # Filter out specific classes and attributes
    names = []

    for td in td_with_links:
        link = td.find('a', title=True)
        if link:
            names.append(link.get_text())

    return names

def get_pageviews_data(page_title):
    # Define parameters
    endpoint = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    project = "en.wikipedia.org"
    access = "all-access"
    agent = "all-agents"  # Changed from "user" to "all-agents" as per example
    article = page_title.replace(" ", "_")  # Replace spaces with underscores
    granularity = "daily"
    start_date = "20150701"
    end_date = datetime.today().strftime("%Y%m%d") + "00"  # Current date at 12am

    # Construct the URL
    url = f"{endpoint}{project}/{access}/{agent}/{article}/{granularity}/{start_date}/{end_date}"

    # Set User-Agent header
    headers = {'User-Agent': 'oliviaseto5@gmail.com'} 

    # Make the API request with a User-Agent header
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve pageviews data. Status code: {response.status_code}")
        return None

def create_pageviews_spreadsheet(page_url):
    # Extract names from the page
    names = extract_names_from_page(page_url)
    if not names:
        print("No names extracted from the page")
        return

    # Create an empty DataFrame to store the combined pageviews data
    combined_df = pd.DataFrame(columns=['id', 'date', 'count'])

    for name in names:
        # Check if the DataFrame is empty or if the name already exists in the combined DataFrame
        if combined_df.empty or name not in combined_df['id'].unique():
            # Get pageviews data for each name
            pageviews_data = get_pageviews_data(name)
            if pageviews_data:
                # Create a DataFrame from the JSON data
                df = pd.DataFrame(pageviews_data['items'])
                # Rename columns
                df.rename(columns={'timestamp': 'date', 'views': 'count'}, inplace=True)
                # Add 'id' column
                df['id'] = name
                # Reorder columns
                df = df[['id', 'date', 'count']]
                # Append to combined DataFrame
                combined_df = combined_df.append(df, ignore_index=True)
        else:
            print(f"Skipping '{name}' as its pageviews data has already been added")

    # Create directory if it doesn't exist
    directory = 'wikipedia_files'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write to Excel file
    page_name = page_url.split("/")[-1].replace("_", " ")
    excel_file_name = f"{page_name}_pageviews.xlsx"
    excel_file_path = os.path.join(directory, excel_file_name)
    combined_df.to_excel(excel_file_path, index=False)
    print(f"Pageviews data saved to {excel_file_path}")

# Tests

# List_of_best-selling_female_music_artists_in_the_United_Kingdom
page_url = "https://en.wikipedia.org/wiki/List_of_best-selling_female_music_artists_in_the_United_Kingdom"
create_pageviews_spreadsheet(page_url)
add_growth_column(os.path.join('wikipedia_files', "List of best-selling female music artists in the United Kingdom_pageviews.xlsx"))
plot_growth_histogram(os.path.join('wikipedia_files', "List of best-selling female music artists in the United Kingdom_pageviews.xlsx"), os.path.join(os.getcwd(), 'wikipedia_files', "List of best-selling female music artists in the United Kingdom_pageviews"))

# List_of_biggest-selling_British_music_artists
page_url = "https://en.wikipedia.org/wiki/List_of_biggest-selling_British_music_artists"
create_pageviews_spreadsheet(page_url)
add_growth_column(os.path.join('wikipedia_files', "List of biggest-selling British music artists_pageviews.xlsx"))
plot_growth_histogram(os.path.join('wikipedia_files', "List of biggest-selling British music artists_pageviews.xlsx"), os.path.join(os.getcwd(), 'wikipedia_files', "List of biggest-selling British music artists_pageviews"))
