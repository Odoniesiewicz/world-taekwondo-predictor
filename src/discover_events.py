import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

URL = "https://results.worldtaekwondo.org/competitions"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

tables = soup.find_all("table")
rows = soup.find_all("tr")
competitions = []
for row in rows:
    row_list = []
    cells = row.find_all("td")
    links = row.find_all("a")
    #print(links)
    results_url = None
    for link in links:
        if link.get_text(strip = True) == "Results":
            results_url = link.get("href")
        
    #print(row.get_text(strip=True))
    for cell in cells:
            #print(cell.get_text(strip=True))
        row_list.append(cell.get_text(strip=True))

    #single day date 
    if re.fullmatch(r"\d{1,2} [A-Za-z]{3} \d{4}",row_list[0]):
        start = datetime.strptime(row_list[0], "%d %b %Y")
        end = datetime.strptime(row_list[0], "%d %b %Y")
        print(start, end)
    #date range but same month
    elif re.fullmatch(r"\d{1,2} - \d{1,2} [A-Za-z]{3} \d{4}", row_list[0]):
        parts = row_list[0].split(" - ")
        parts_2 = parts[1].split(" ",1)
        start = datetime.strptime(parts[0] + " " + parts_2[1], "%d %b %Y")
        end = datetime.strptime(parts[1], "%d %b %Y")
        print(start, end)
    #date range but different month
    elif re.fullmatch(r"\d{1,2} [A-Za-z]{3} - \d{1,2} [A-Za-z]{3} \d{4}", row_list[0]):
        parts = row_list[0].split(" - ")
        parts_2 = parts[1].split()
        #check for year change
        if ((parts[0].split()[1].lower() == "dec" ) and (parts_2[1].lower() == "jan")):
            start = datetime.strptime(parts[0] + " " + str(int(parts_2[2]) -1), "%d %b %Y")
        else:
            start = datetime.strptime(parts[0] + " " + parts_2[2], "%d %b %Y")
        end = datetime.strptime(parts[1], "%d %b %Y")
        print(start, end)
    elif re.fullmatch(r"\d{4}", row_list[0]):
        start = None
        end = None
        print(start,end)
    competition = {
    "start_date" : start,
    "end_date" : end,
    "name" : row_list[2],
    "url"  : results_url
    }
    competitions.append(competition)
#for i in range(len(competitions)):
    
    #print(competitions[i]["date"])
#print(datetime.strptime("4 Sep 2026", "%d %b %Y"))
#print(competitions)
#print(competitions_data)