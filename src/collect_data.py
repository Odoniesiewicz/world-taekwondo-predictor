import requests
from bs4 import BeautifulSoup

def results_scraper(start_date, end_date, name, url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    rows=soup.find_all("tr")
    current_round = None
    current_weight = None
    fight_records = []
    for row in rows:
        cells = row.find_all("td")
        row_list = []
        winner=None
        if "winner" in cells[3].get("class", []) :
            winner = cells[3].get_text(strip=True)
        else:
            winner = cells[6].get_text(strip=True)
        for cell in cells:
            row_list.append(cell.get_text(strip=True))
        #carrying forward round from previous row if doesnt have it specified
        if (len(row_list[0])!=0):
            current_round = row_list[0]
        else:
            row_list[0] = current_round
        #carrying forward weight from previous row if doesnt have it specified
        if len(row_list[1])!=0:
            current_weight = row_list[1]
        else:
            row_list[1] = current_weight
        #build fight dictionary
        fight = {
            "round" : row_list[0],
            "weight_category" : row_list[1],
            "fighter_a_country" : row_list[2],
            "fighter_a" : row_list[3],
            "score" : row_list[4],
            "method" : row_list[5],
            "fighter_b" : row_list[6],
            "fighter_b_country" : row_list[7],
            "winner" : winner,
            "event_name" : name,
            "start_date" : start_date,
            "end_date" : end_date
        }
        fight_records.append(fight)

    return fight_records
