import requests
from bs4 import BeautifulSoup
import csv

# URL of the website
url = 'https://gasprices.aaa.com/state-gas-price-averages/'

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table by its id
table = soup.find('table', id='sortable')

# Initialize a list to store all gas prices
gas_prices = []

# Iterate through each row in the table body (skip the header)
for row in table.find('tbody').find_all('tr'):
    # Extract the text from each cell in the row
    cells = row.find_all('td')
    
    # Assuming the first cell is the state name and the rest are prices
    state = cells[0].text.strip()
    regular_price = cells[1].text.strip()
    mid_grade_price = cells[2].text.strip()
    premium_price = cells[3].text.strip()
    diesel_price = cells[4].text.strip()
    
    # Append the data to the list
    gas_prices.append([state, regular_price, mid_grade_price, premium_price, diesel_price])

# Optionally, write the data to a CSV file
with open('gas_prices.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'Regular', 'Mid-Grade', 'Premium', 'Diesel'])  # Header
    writer.writerows(gas_prices)

print("Gas prices data extracted and saved to gas_prices.csv")
