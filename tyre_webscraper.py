import sqlite3
import pandas as pd
import requests  
from bs4 import BeautifulSoup  
import numpy as np 
import csv
import time 
import random  
import datetime

currTime = datetime.datetime.now()

def split_first(text):
    # strip leading/trailing whitespace, then split into at most 2 parts
    parts = text.strip().split(' ', 1)
    first = parts[0]
    rest  = parts[1] if len(parts) > 1 else ''
    return first, rest


# to implement replace the second half of the text with an input method for dimensions and postcode
site = 'https://www.national.co.uk'  

append = '/tyres-search/' 
width = '205' 
aspectRatio = '55' 
rimSize = '16'   
postcode = '?pc=HU74DL'

Isheader = True
def Tyre_database_national(site, append, width, aspectRatio, rimSize, postcode, isHeader):
    fullWebsite = site + append + width + '-' + aspectRatio + '-' + rimSize + postcode
    # website = 'https://www.national.co.uk/tyres-search/205-55-16?pc=HU74DL'  
    csv_file = 'Tyres.csv'

    print(fullWebsite)
    r = requests.get(fullWebsite) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    prices = soup.find_all('span', class_='red text-24')  
    patterns = soup.find_all('a', class_='pattern_link') 
    formattedPrice = []   
    formattedPatterns = []

    for price in prices:  
        formattedPrice.append(price.text)

    for pattern in patterns:   
        formattedPatterns.append(pattern.text) 

    # Create a CSV file and write the header and data
    with open(csv_file, 'a', newline='') as file:  
        writer = csv.DictWriter(file, fieldnames=['Website', 'Name', 'Width', 'Aspect ratio', 'Rim size', 'Pattern', 'Price', 'Time'])
        if isHeader:
            writer.writeheader()
        for i in range(0, len(formattedPrice)):    
            imageName = 'PageContent_ucTyreResults_rptTyres_imgBrand_' 
            imageName = imageName + str(i)   
            img_tag = soup.find('img', id=imageName)
            brandName = img_tag.get('alt')

            res = " ".join(str(formattedPrice[i]).split())
            row = {'Website' : str(site), 'Name' : str(brandName), 'Width' : str(width) , 'Aspect ratio' : str(aspectRatio) , 'Rim size' : str(rimSize) , 'Pattern' : str(formattedPatterns[i])  , 'Price' : str(res), 'Time' : str(currTime)}
            writer.writerow(row) 

    conn = sqlite3.connect('Tyres.db') 
    c = conn.cursor()  
    df = pd.read_csv(csv_file, encoding='ISO-8859-1') 
    df.info()
    df.to_sql('Tyres', conn, if_exists='replace', index=False) 

def Tyre_database_blackcircles(site, append, width, aspectRatio, rimSize, postcode, isHeader):
    fullWebsite = site + append + width + '-' + aspectRatio + '-' + rimSize 
    # website = 'https://www.blackcircles.com/tyres/205-55-16'  
    csv_file = 'Tyres.csv'

    print(fullWebsite)
    r = requests.get(fullWebsite) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    prices = soup.find_all('div', class_='tyrePrice')   
    patterns = soup.find_all('p', class_='model-size')  
    # names = soup.find_all('span', class_='tyreNameWrap')  
    #Since the class is a span, strip is used to remove any extra spaces
    names = [s.get_text(strip=True) for s in soup.find_all('span', class_='tyreNameWrap')] 

    formattedPrice = []   
    formattedPatterns = []  
    formattedNames = []

    
    for price in prices:  
        formattedPrice.append(price.text)

    # Split the names into tyre name and pattern
    for name in names:    
        first, rest = split_first(name) 
        formattedNames.append(first)
        formattedPatterns.append(rest)  
    
    # Create a CSV file and write the header and data
    with open(csv_file, 'a', newline='') as file:  
        writer = csv.DictWriter(file, fieldnames=['Website', 'Name', 'Width', 'Aspect ratio', 'Rim size', 'Pattern', 'Price', 'Time'])
        if isHeader:
            writer.writeheader()
        for i in range(0, len(formattedPrice)):    
            res = " ".join(str(formattedPrice[i]).split())
            row = {'Website' : str(site), 'Name' : str(formattedNames[i]), 'Width' : str(width) , 'Aspect ratio' : str(aspectRatio) , 'Rim size' : str(rimSize) , 'Pattern' : str(formattedPatterns[i])  , 'Price' : str(res), 'Time' : str(currTime)}
            writer.writerow(row) 

    conn = sqlite3.connect('Tyres.db') 
    c = conn.cursor()  
    df = pd.read_csv(csv_file, encoding='ISO-8859-1') 
    df.info()
    df.to_sql('Tyres', conn, if_exists='replace', index=False)


site = 'https://www.national.co.uk'   
append = '/tyres-search/'
Tyre_database_national(site, append, '205', '55', '16', postcode, True) 
time.sleep(random.randint(10, 30)) 
Tyre_database_national(site, append, '225', '50', '16', postcode, False) 
time.sleep(random.randint(10, 30)) 
Tyre_database_national(site, append, '185', '16', '14', postcode, False) 

site = 'https://www.blackcircles.com'   
append = '/tyres/'
Tyre_database_blackcircles(site, append, '205', '55', '16', postcode, False) 
time.sleep(random.randint(10, 30)) 
Tyre_database_blackcircles(site, append, '225', '50', '16', postcode, False) 
time.sleep(random.randint(10, 30)) 
Tyre_database_blackcircles(site, append, '185', '16', '14', postcode, False) 