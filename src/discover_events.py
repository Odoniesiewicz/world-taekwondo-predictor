import requests
import re
import pandas as pd
from collect_data import results_scraper
from datetime import datetime
from bs4 import BeautifulSoup

URL = "https://results.worldtaekwondo.org/competitions"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

rows = soup.find_all("tr")
competitions = []
for row in rows:
    row_list = []
    cells = row.find_all("td")
    links = row.find_all("a")
    results_url = None
    start = None
    end = None
    for link in links:
        if link.get_text(strip = True) == "Results":
            results_url = link.get("href")

    for cell in cells:
        row_list.append(cell.get_text(strip=True))

    #single day date 
    if re.fullmatch(r"\d{1,2} [A-Za-z]{3} \d{4}",row_list[0]):
        start = datetime.strptime(row_list[0], "%d %b %Y")
        end = datetime.strptime(row_list[0], "%d %b %Y")

    #date range but same month
    elif re.fullmatch(r"\d{1,2} - \d{1,2} [A-Za-z]{3} \d{4}", row_list[0]):
        parts = row_list[0].split(" - ")
        parts_2 = parts[1].split(" ",1)
        start = datetime.strptime(parts[0] + " " + parts_2[1], "%d %b %Y")
        end = datetime.strptime(parts[1], "%d %b %Y")

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
    elif re.fullmatch(r"\d{4}", row_list[0]):
        start = None
        end = None

    #flag possible mistakes in the data
    match = re.search(r"\d{4}", row_list[2])
    if match:
        year_from_name = int(match.group())
    else:
        year_from_name = None
    if start and end:
        if (start > end ):
            print(f"{row_list[2]} , POSSIBLE ERROR")
        if(((year_from_name != start.year) and (year_from_name != end.year)) and year_from_name is not None):
            print(f" WARNING :POSSIBLE ERROR, {row_list[2]}, {start}, {end}")
    competition = {
    "start_date" : start,
    "end_date" : end,
    "name" : row_list[2],
    "url"  : results_url
    }

    competitions.append(competition)
all_fights = []
failed_events = []
for competition in competitions:
    if competition["url"]:
        try:
            fights = results_scraper(competition["start_date"], competition["end_date"], competition["name"], competition["url"])
            all_fights.extend(fights)
        except Exception as error:
            print(f"failed: {competition["name"]} has {error}")
            failed_events.append(competition)

df = pd.DataFrame(all_fights)
for event in failed_events:
    print(event["name"], "-", event["url"])

df.to_csv("data/raw/world_taekwondo_fights_raw.csv", index = False)