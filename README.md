# Web Scraping digidb.io and Transform it into MySQL Database

Halo, Assalamu'alaykum..

Hari ini saya akan share mengenai quiz hari ini, yaitu mengubah table dari hasil web scraping menjadi satu buah database dari website digimon.db

![alt text](https://github.com/ridhoaryo/20_21_Notes_JCDS_Module_2_Purwadhika/blob/master/database.jpg "Database Result")

## Let's brakedown the code
## 1. Import the library
```
import mysql.connector
import requests
from bs4 import BeautifulSoup
```

## 2. Web Scraping from digidb.io
```
web = requests.get('http://digidb.io/digimon-list/')
data = BeautifulSoup(web.content, 'html.parser')

table = data.find('table', id='digiList')
tbody = table.find('tbody')
img = tbody.find_all('img')

# ============== HEADER ==============
header_list = []
header = table.find('tr', class_='header')

th = header.find_all('th')
for i in th:
    header_list.append(i.text)
header_list.append('Image link')

# ============== IMAGE LINK ==============
image_list = []
for i in img:
    image_list.append(i['src'])

# ============== DIGIMON ==============
digimon_list = []
digi = tbody.find_all('a')
for i in digi:
    digimon_list.append(i.text)

# ============== NUMBER ==============
number_list = []
for i in range(1,len(digimon_list)+1):
    number_list.append(i)

# ============== DIGIMON'S ATTRIBUTES ==============
attribute_list = []
att = tbody.find_all('center')
for i in att:
    attribute_list.append(i.text)

# ============== GROUPING EACH ATTRIBUTE ==============
grouped_attributes = []
j = 0
for i in range(11,3762,11):
    grouped_attributes.append(attribute_list[j:i])
    j += 11

# ============== COMBINING LIST ==============
for i in range(len(grouped_attributes)):
    grouped_attributes[i].append(image_list[i])
    grouped_attributes[i].insert(0,digimon_list[i])
    grouped_attributes[i].insert(0,number_list[i])
```

## 3. Make it as list of tuples
```
grouped_attributes_set = []
for i in grouped_attributes:
    grouped_attributes_set.append(tuple(i))
```

## 4. Database computing
```
db = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'ridhoaryo',
    passwd = '********', 
    database = 'digimon'
)
c = db.cursor()
# ===== MAKE DATABASE =====
# c.execute('create database digimon')

# ===== MAKE TABLE =====
# c.execute('create table digimon(no text, Digimon text, Stage text, Type text, Attribute text, Memory text, Equip_Slots text, HP text, SP text, Atk text, Def text, intx text, Spd text)')

# ===== ADD NEW COLUMN 'image_link' =====
# c.execute('alter table digimon add column image_link text after Spd')

# ===== MODIFY 'no' COLUMN =====
# c.execute('alter table digimon modify column no int')

# ===== RENAMING 'int' COLUMN TO Int_ =====
# c.execute('alter table digimon rename column intx to Int_')

```
## 5. Insert the data into table
```
sql = 'insert into digimon (no, Digimon, Stage, Type, Attribute, Memory, Equip_Slots, HP, SP, Atk, Def, intx, Spd, image_link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
c.executemany(sql, grouped_attributes_set)
db.commit()
```
