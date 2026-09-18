import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/world_taekwondo_fights_clean.csv", parse_dates=["start_date", "end_date"])

df = df.sort_values("start_date")

print(df[["start_date","event_name"]].head())
fighter_history = {}
feature_rows = []

for (start_date, event_name), tournament_fights in df.groupby(["start_date", "event_name"], sort=False):
    for index, fight in tournament_fights.iterrows():
        fighter_a = fight["fighter_a"]
        fighter_b = fight["fighter_b"]

        #check if fighter has had previous fights recorded
        if fighter_a in fighter_history:
            a_previous_fights = fighter_history[fighter_a]["fights"]
            a_previous_wins = fighter_history[fighter_a]["wins"]
        else:
            a_previous_fights = 0
            a_previous_wins = 0
        if fighter_b in fighter_history:
            b_previous_fights = fighter_history[fighter_b]["fights"]
            b_previous_wins = fighter_history[fighter_b]["wins"]
        else:
            b_previous_fights = 0
            b_previous_wins = 0
        if a_previous_fights > 0 :
             a_win_rate = a_previous_wins/a_previous_fights
        else:
             a_win_rate = 0
        if b_previous_fights > 0 :
             b_win_rate = b_previous_wins/b_previous_fights
        else:
             b_win_rate = 0

        #recent form 
        if fighter_a in fighter_history:
            a_recent_results = fighter_history[fighter_a]["results"][-5:]
        else:
            a_recent_results = []
        if fighter_b in fighter_history:
            b_recent_results = fighter_history[fighter_b]["results"][-5:]
        else:
            b_recent_results = []
        if len(a_recent_results) > 0:
            a_recent_win_rate = sum(a_recent_results) / len(a_recent_results)
        else: 
            a_recent_win_rate = 0
        if len(b_recent_results) > 0:
            b_recent_win_rate = sum(b_recent_results) / len(b_recent_results)
        else: 
            b_recent_win_rate = 0
        win_rate_difference = a_win_rate - b_win_rate
        recent_form_difference = a_recent_win_rate - b_recent_win_rate
        experience_difference = a_previous_fights - b_previous_fights

        if fighter_a in fighter_history:
            a_last_fight_date = fighter_history[fighter_a]["last_fight_date"]
        else:
            a_last_fight_date = None
        if fighter_b in fighter_history:
            b_last_fight_date = fighter_history[fighter_b]["last_fight_date"]
        else:
            b_last_fight_date = None
        if a_last_fight_date is not None:
            a_days_since_last_fight = (start_date - a_last_fight_date).days
        else:
            a_days_since_last_fight = np.nan
        if b_last_fight_date is not None:
            b_days_since_last_fight = (start_date - b_last_fight_date).days
        else:
            b_days_since_last_fight = np.nan
        if fight["winner"] == fighter_a:
            winner_is_a = 1
        else:
             winner_is_a = 0
        if pd.notna(a_days_since_last_fight) and pd.notna(b_days_since_last_fight):
            days_since_last_fight_difference = (a_days_since_last_fight - b_days_since_last_fight)
        else:
            says_since_last_fight_difference = np.nan
        
        feature_rows.append({
            "start_date" : start_date,
            "event_name" : event_name,
            "fighter_a" : fighter_a,
            "fighter_b" : fighter_b,
            "a_previous_fights" : a_previous_fights,
            "b_previous_fights" : b_previous_fights,
            "a_previous_wins" : a_previous_wins,
            "b_previous_wins" : b_previous_wins,
            "a_win_rate": a_win_rate,
            "b_win_rate": b_win_rate,
            "winner_is_a" : winner_is_a,
            "a_recent_win_rate" : a_recent_win_rate,
            "b_recent_win_rate" : b_recent_win_rate,
            "win_rate_difference" : win_rate_difference,
            "recent_form_difference" : recent_form_difference,
            "experience_difference" : experience_difference,
            "a_days_since_last_fight" : a_days_since_last_fight,
            "b_days_since_last_fight" : b_days_since_last_fight,
            "days_since_last_fight_difference" : b_days_since_last_fight
             }
        )
        #print(fighter_a, a_previous_fights, a_previous_wins, a_win_rate, "|||", fighter_b, b_previous_fights, b_previous_wins, b_win_rate)

    for index, fight in tournament_fights.iterrows():
        fighter_a = fight["fighter_a"]
        fighter_b = fight["fighter_b"]
        

        if fighter_a not in fighter_history:
            fighter_history[fighter_a] = {"fights" : 0, "wins" : 0, "results" : [], "last_fight_date" : None}
        if fighter_b not in fighter_history:
            fighter_history[fighter_b] = {"fights" : 0, "wins" : 0, "results" : [], "last_fight_date" : None}

        #increment fight number
        fighter_history[fighter_a]["fights"] += 1
        fighter_history[fighter_b]["fights"] += 1

        winner = fight["winner"]

        if winner == fighter_a:
            fighter_history[fighter_a]["wins"] +=1
            fighter_history[fighter_a]["results"].append(1)
            fighter_history[fighter_b]["results"].append(0)

        elif winner == fighter_b:
            fighter_history[fighter_b]["wins"] +=1
            fighter_history[fighter_b]["results"].append(1)
            fighter_history[fighter_a]["results"].append(0)

        fighter_history[fighter_a]["last_fight_date"] = start_date
        fighter_history[fighter_b]["last_fight_date"] = start_date


features_df = pd.DataFrame(feature_rows)
print(features_df.head())
print(features_df.shape)
print(features_df["winner_is_a"].value_counts())
print(features_df["winner_is_a"].mean())