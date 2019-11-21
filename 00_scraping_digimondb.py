import requests
from bs4 import BeautifulSoup
import xlsxwriter
import csv
import json

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

# ============== ADD HEADER LIST ==============
grouped_attributes.insert(0, header_list)


# ============== WRITE TO EXCEL ==============
digimon_xlsx = xlsxwriter.Workbook('Digimon.xlsx')
sheet1 = digimon_xlsx.add_worksheet('Digimon List')
for r in range(len(grouped_attributes)):
    for c in range(len(header_list)):
        sheet1.write(r,c,grouped_attributes[r][c])

digimon_xlsx.close()

# ============== ZIPING THE LIST INTO DICT ==============
digimon_all = []
header_only = grouped_attributes[0]
content = grouped_attributes[1:]
for i in range(len(content)):
    data = dict(zip(header_only, content[0:][i]))
    digimon_all.append(data)

print(digimon_all[0])
# # ============== WRITE TO JSON ==============
with open('Digimon.json', 'w') as my_digimon:
    json.dump(digimon_all, my_digimon)

# # ============== WRITE TO CSV ==============
with open('Digimon.csv', 'w', newline='') as digimon_csv:
    column = header_only
    write = csv.DictWriter(digimon_csv, fieldnames=column)
    write.writeheader()
    write.writerows(digimon_all)
