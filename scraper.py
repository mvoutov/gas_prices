from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# Create an HTML Session object
session = HTMLSession()

# Use the session to get the web page
response = session.get('https://gasprices.aaa.com/state-gas-price-averages/')

# Render the page, this will execute JavaScript
response.html.render()

# Parse the rendered HTML with BeautifulSoup
soup = BeautifulSoup(response.html.html, 'html.parser')

table = soup.find('table', id='sortable')
#print(table)

# Get today's date
today = datetime.today()

# Get today's date in a string format suitable for file naming
date_string = today.strftime("%Y-%m-%d")

# Initialize a list to store all gas prices
gas_prices = []

# Iterate through each row in the table body
for row in table.find('tbody').find_all('tr'):
    # Extract the text from each cell in the row
    cells = row.find_all('td')
    
    # First cell is the state name and the rest are prices
    state = cells[0].text.strip()
    regular_price = cells[1].text.strip()
    mid_grade_price = cells[2].text.strip()
    premium_price = cells[3].text.strip()
    diesel_price = cells[4].text.strip()
    
    # Append the data to the list
    gas_prices.append([
        state,
        regular_price,
        mid_grade_price,
        premium_price,
        diesel_price,
        today.strftime("%d"),   # Day
        today.strftime("%m"),   # Month
        today.strftime("%Y"),    # Year
        date_string
    ])



# Define the filename for today's data
todays_filename = f'gas_prices_daily_csv/gas_prices_{date_string}.csv'

# Write the data to a CSV file
with open(todays_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'Regular', 'Mid-Grade', 'Premium', 'Diesel', 'Day', 'Month', 'Year', 'Date'])  # Header
    writer.writerows(gas_prices)

print(f"Today's gas prices data saved to {todays_filename}")

# Now append today's data to the master CSV file
master_filename = 'gas_prices.csv'

# # Open the master file in append mode and write today's data
# with open(master_filename, 'a', newline='', encoding='utf-8') as master_file:
#     writer = csv.writer(master_file)
#     writer.writerows(gas_prices)

# print(f"Today's gas prices data appended to {master_filename}")

# Check if today's data is already in the master file
already_recorded = False
if os.path.isfile(master_filename):
    with open(master_filename, 'r', newline='', encoding='utf-8') as master_file:
        existing_data = csv.reader(master_file)
        for row in existing_data:
            if date_string in row:
                already_recorded = True
                break

# If today's data is not already recorded, append it to the master file
if not already_recorded:
    with open(master_filename, 'a', newline='', encoding='utf-8') as master_file:
        writer = csv.writer(master_file)
        writer.writerows(gas_prices)
    print(f"Today's gas prices data appended to {master_filename}")
else:
    print(f"Today's data is already recorded in {master_filename}. No action taken.")