#importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# empty lists for data storage
initial_description = []
initial_price = []

#handling pagination
for page in range(1,51):
    response = requests.get(f'https://www.jumia.com.ng/catalog/?q=samsung+phones&page={page}#catalog-listing')
    soup =BeautifulSoup(response.text, 'html.parser')

    #scraping description data
    x = [desc.text for desc in soup.find_all('h3', class_ ='name')]
    initial_description.append(x)
    #scraping price data
    y =  [pricee.text for pricee in soup.find_all('div', class_ = 'prc')]
    initial_price.append(y)

#creating a single list from a list of sublists
description = [i for item1 in initial_description for i in item1]
price = [j for item2 in initial_price for j in item2]

#creating a pandas table
table = pd.DataFrame({"Description" : description, "Price" : price})

#removing special characters from the price column
table.Price.replace(regex=True, inplace=True, to_replace=r'[^0-9.\-]', value=r'')

#to get rid of the empty rows in the table
table = table[(table.Price !='') & (table.Description !='')]

#resetting table index
table = table.reset_index(drop=True)

#saving data in a csv format
table.to_csv('samsung.csv', index=False)