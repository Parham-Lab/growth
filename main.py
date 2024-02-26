from file import rename_and_keep_columns, add_growth_column, add_count_cleaned_column, add_growth_cleaned_column, plot_growth_histogram

# CSVs that are properly formated, population is equivalent to count
# csv_names = {"urban-and-rural-population":['Year','Code','Urban population'], # good example
#               "landline-phone-subscriptions":['Year','Code','Fixed telephone subscriptions'], # good example
#               "number-of-births-per-year":['Year','Code','Births - Sex: all - Age: all - Variant: estimates'], # good example
#               "number-of-deaths-per-year":['Year','Code','Deaths - Sex: all - Age: all - Variant: estimates'], # good example
#               "monthly-co2-emissions-from-international-and-domestic-flights":['Day','Code','Monthly CO₂ emissions from domestic aviation'], # good example
#               "annual-co2-emissions-per-country":['Year','Code','Annual CO₂ emissions'], # good example
#               "coal-production-by-country":['Year','Code','Coal production (TWh)'], # good example
#               "fertilizer-consumption-usda":['Year','Code','fertilizer_quantity'], # good example    
#               "primary-energy-cons":['Year','Code','Primary energy consumption (TWh)'], # good example   
#               "milk-production-tonnes":['Year','Code','Milk | 00001780 || Production | 005510 || tonnes'], # good example   
#               "seafood-and-fish-production-thousand-tonnes":['Year','Code','Freshwater Fish | 00002761 || Production | 005511 || tonnes'], # good example  
#               "meat-production-tonnes":['Year','Code','Meat, total | 00001765 || Production | 005510 || tonnes'], # good example  
#               } 

# CSVs that are properly formated, but need to calculate population because the count of population is cumulative
csv_names = {"cumulative-covid-vaccinations":['Day','Code','total_vaccinations'], # right skewed
                "people-vaccinated-covid":['Day','Code','people_vaccinated'], # right skewed
                "cumulative-covid-vaccine-booster-doses":['Day','Code','total_boosters'], # right skewed
                "full-list-total-tests-for-covid-19":['Day','Code','total_tests'], # right skewed
                "us-total-covid-vaccine-doses-distributed":['Day','Entity','total_distributed'], # right skewed
                "cumulative-co-emissions":['Year','Code','Cumulative CO₂ emissions'], # right skewed
            }

for csv, columns in csv_names.items():
    original_csv_path = "original_csv" + "/" + csv + ".csv"
    modified_csv_path = "modified_csv" + "/" + csv + ".csv"
    graph_path = "graphs" + "/" + csv

    columns_to_keep_and_rename = {columns[0]: 'date', columns[1]: 'id', columns[2]:'count'}

    rename_and_keep_columns(original_csv_path, columns_to_keep_and_rename, modified_csv_path)
    # add_growth_column(modified_csv_path)
    add_count_cleaned_column(modified_csv_path)
    add_growth_cleaned_column(modified_csv_path)
    plot_growth_histogram(modified_csv_path, graph_path)
    