import requests
from bs4 import BeautifulSoup

URL = "https://results.worldtaekwondo.org/competitions/2024-paris-olympic-games/results"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")
##print(response.status_code)
##print(len(response.text))
#print(response.text[:500])
tables = soup.find_all("table")
rows=soup.find_all("tr")
#print(len(rows))
#print(response.url)
#print(response.history)
#tables = soup.find_all("table")
row = rows[1]
lis=[]
current_round = None
current_weight = None
fight_records = []
for row in rows[0:5]:
    cells = row.find_all("td")
    row_list = []
    for cell in cells:
        row_list.append(cell.get_text(strip=True))
        #print(cell.get_text(strip=True))
    if (len(row_list[0])!=0):
        current_round = row_list[0]
    else:
        row_list[0] = current_round
    if len(row_list[1])!=0:
        current_weight = row_list[1]
    else:
        row_list[1] = current_weight
    fight = {
        "round" : row_list[0],
        "weight_category" : row_list[1],
        "fighter_a_country" : row_list[2],
        "fighter_a" : row_list[3],
        "score" : row_list[4],
        "method" : row_list[5],
        "fighter_b" : row_list[6],
        "fighter_b_country" : row_list[7]
    }
    fight_records.append(fight)
    #lis.append(row_list)
    #print(len(row_list), row_list)
#print(lis)
print(fight_records)