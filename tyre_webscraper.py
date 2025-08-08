import requests  
from bs4 import BeautifulSoup  
import numpy as np 
import csv
 
# to implement replace the second half of the text with an input method for dimensions and postcode
website = 'https://www.national.co.uk/tyres-search/205-55-16?pc=HU74DL'  
csv_file = 'national_tyres.csv'

r = requests.get(website) 
soup = BeautifulSoup(r.text, 'html.parser') 
prices = soup.find_all('span', class_='red text-24')  
names = soup.find_all('div', class_='tyreresult')  
patterns = soup.find_all('a', class_='pattern_link') 
print(prices) 
print(patterns)
formattedPrice = []   
formattedPatterns = []

for price in prices:  
    formattedPrice.append(price.text)

for pattern in patterns:   
    formattedPatterns.append(pattern.text) 

for name in names: 
    print(name.text) 

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['pattern', 'price'])
    writer.writeheader()
    for i in range(0, len(formattedPrice)):   
        res = " ".join(str(formattedPrice[i]).split())
        row = {'pattern' : str(formattedPatterns[i])  , 'price' : str(res)}
        writer.writerow(row)