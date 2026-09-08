import requests
import pandas as pd
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
current_round = None
current_weight = None
fight_records = []
for row in rows:
    cells = row.find_all("td")
    row_list = []
    winner=None
    #print(cells[3].get("class"), cells[6].get("class"))
    if "winner" in cells[3].get("class", []) :
        winner = cells[3].get_text(strip=True)
    else:
        winner = cells[6].get_text(strip=True)
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
        "fighter_b_country" : row_list[7],
        "winner" : winner
    }
    fight_records.append(fight)
df = pd.DataFrame(fight_records)
#cleaned_df = 
#print(df.shape)
#print(df.columns)
#print(df.head())
#print(df.groupby("weight_category").size())
#print(df["round"].unique())
#print(df["weight_category"].unique())
#print(df.isna().sum())
invalid_winners = (df["winner"] == "")


df=df[~invalid_winners]
print((df == "").sum())
df.to_csv("data/raw/paris_2024_fights_clean.csv", index=False)
