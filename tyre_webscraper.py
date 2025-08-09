import requests  
from bs4 import BeautifulSoup  
import numpy as np 
import csv
 
# to implement replace the second half of the text with an input method for dimensions and postcode
site = 'https://www.national.co.uk'  

append = '/tyres-search/' 
width = '205' 
aspectRatio = '55' 
rimSize = '16'  

fullWebsite = site + append + '-' + width + '-' + aspectRatio + '-' + rimSize
website = 'https://www.national.co.uk/tyres-search/205-55-16?pc=HU74DL'  
csv_file = 'national_tyres.csv'

r = requests.get(website) 
soup = BeautifulSoup(r.text, 'html.parser') 
prices = soup.find_all('span', class_='red text-24')  
names = soup.find_all('div', class_='details')  
patterns = soup.find_all('a', class_='pattern_link') 
print(names)
formattedPrice = []   
formattedPatterns = []

for price in prices:  
    formattedPrice.append(price.text)

for pattern in patterns:   
    formattedPatterns.append(pattern.text) 

# Create a CSV file and write the header and data
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Website', 'Name', 'Width', 'Aspect ratio', 'Rim size', 'Pattern', 'Price'])
    writer.writeheader()
    for i in range(0, len(formattedPrice)):    
        imageName = 'PageContent_ucTyreResults_rptTyres_imgBrand_' 
        imageName = imageName + str(i)   
        img_tag = soup.find('img', id=imageName)
        brandName = img_tag.get('alt')

        res = " ".join(str(formattedPrice[i]).split())
        row = {'Website' : str(site), 'Name' : str(brandName), 'Width' : str(width) , 'Aspect ratio' : str(aspectRatio) , 'Rim size' : str(rimSize) , 'Pattern' : str(formattedPatterns[i])  , 'Price' : str(res)}
        writer.writerow(row)