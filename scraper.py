from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Create an HTML Session object
session = HTMLSession()

# Use the session to get the web page
response = session.get('https://gasprices.aaa.com/state-gas-price-averages/')

# Render the page, this will execute JavaScript
response.html.render()

# Parse the rendered HTML with BeautifulSoup
soup = BeautifulSoup(response.html.html, 'html.parser')

table = soup.find('table', id='sortable')
print(table)

# Get today's date
today = datetime.today()

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
        today.strftime("%Y")    # Year
    ])

# Write the data to a CSV file
with open('gas_prices.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'Regular', 'Mid-Grade', 'Premium', 'Diesel', 'Day', 'Month', 'Year'])  # Header
    writer.writerows(gas_prices)