from file import rename_and_keep_columns, add_growth_column, add_count_cleaned_column, add_growth_cleaned_column, plot_growth_histogram, reformat_excel, reformat_excel_dates_as_row_strip_year

# CSVs that are properly formated, population is equivalent to count
# csv_names = {"urban-and-rural-population":['Year','Code','Urban population'], 
#               "landline-phone-subscriptions":['Year','Code','Fixed telephone subscriptions'], 
#               "number-of-births-per-year":['Year','Code','Births - Sex: all - Age: all - Variant: estimates'], 
#               "number-of-deaths-per-year":['Year','Code','Deaths - Sex: all - Age: all - Variant: estimates'], 
#               "monthly-co2-emissions-from-international-and-domestic-flights":['Day','Code','Monthly CO₂ emissions from domestic aviation'], # good example
#               "annual-co2-emissions-per-country":['Year','Code','Annual CO₂ emissions'], 
#               "coal-production-by-country":['Year','Code','Coal production (TWh)'], 
#               "fertilizer-consumption-usda":['Year','Code','fertilizer_quantity'],    
#               "primary-energy-cons":['Year','Code','Primary energy consumption (TWh)'],  
#               "milk-production-tonnes":['Year','Code','Milk | 00001780 || Production | 005510 || tonnes'], 
#               "seafood-and-fish-production-thousand-tonnes":['Year','Code','Freshwater Fish | 00002761 || Production | 005511 || tonnes'], # good example  
#               "meat-production-tonnes":['Year','Code','Meat, total | 00001765 || Production | 005510 || tonnes'], 
#               } 

# for csv, columns in csv_names.items():
#     original_csv_path = "original_csv" + "/" + csv + ".csv"
#     modified_csv_path = "modified_csv" + "/" + csv + ".csv"
#     graph_path = "graphs" + "/" + csv

#     columns_to_keep_and_rename = {columns[0]: 'date', columns[1]: 'id', columns[2]:'count'}

#     rename_and_keep_columns(original_csv_path, columns_to_keep_and_rename, modified_csv_path)
#     add_growth_column(modified_csv_path)
#     plot_growth_histogram(modified_csv_path, graph_path)

# CSVs that are properly formated, but need to calculate population because the count of population is cumulative
# csv_names = {"cumulative-covid-vaccinations":['Day','Code','total_vaccinations'],
#                 "people-vaccinated-covid":['Day','Code','people_vaccinated'], 
#                 "cumulative-covid-vaccine-booster-doses":['Day','Code','total_boosters'], 
#                 "full-list-total-tests-for-covid-19":['Day','Code','total_tests'],
#                 "us-total-covid-vaccine-doses-distributed":['Day','Entity','total_distributed'], 
#                 "cumulative-co-emissions":['Year','Code','Cumulative CO₂ emissions'], 
#             }

# for csv, columns in csv_names.items():
#     original_csv_path = "original_csv" + "/" + csv + ".csv"
#     modified_csv_path = "modified_csv" + "/" + csv + ".csv"
#     graph_path = "graphs" + "/" + csv

#     columns_to_keep_and_rename = {columns[0]: 'date', columns[1]: 'id', columns[2]:'count'}

#     rename_and_keep_columns(original_csv_path, columns_to_keep_and_rename, modified_csv_path)
#     add_growth_column(modified_csv_path)
#     add_count_cleaned_column(modified_csv_path)
#     add_growth_cleaned_column(modified_csv_path)
#     plot_growth_histogram(modified_csv_path, graph_path)

# XLSX files from Sage Data
# file_names = ["airport_arrivals_sage", "airport_departures_sage", "crop_production_sage", "commodity_balances_tobacco_sage", 
#               "average_daily_inmate_population_sage", "peak_inmate_population_sage", "crimes_reported_sage", "recruiting_expenses_sage"
#               "current_account_countries_sage", "expenses_countries_sage", "revenues_countries_sage", "labor_markets_countries_sage",
#               "total_us_troop_deployment_sage", "total_federal_aid_counties_sage", "population_countries_sage", "state_government_tax_revenue_sage"]

# for file in file_names:
#     original_csv_path = "original_csv" + "/" + file + ".xlsx"
#     modified_csv_path = "modified_csv" + "/" + file + ".xlsx"
#     graph_path = "graphs" + "/" + file
#     reformat_excel(original_csv_path, modified_csv_path)
#     add_growth_column(modified_csv_path)
#     plot_growth_histogram(modified_csv_path, graph_path)

# xlsx = "recruiting_expenses_sage"
# original_csv_path = "original_csv" + "/" + xlsx + ".xlsx"
# modified_csv_path = "modified_csv" + "/" + xlsx + ".xlsx"
# graph_path = "graphs" + "/" + xlsx
# reformat_excel_dates_as_row_strip_year(original_csv_path, modified_csv_path)
# add_growth_column(modified_csv_path)
# plot_growth_histogram(modified_csv_path, graph_path)