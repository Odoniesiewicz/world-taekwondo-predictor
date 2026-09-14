import pandas as pd

df = pd.read_csv("data/raw/world_taekwondo_fights_raw.csv")
#adding the manual dates for these Olympic games as werent entered in the data set
olympic_date_fixes = {
    "Sydney 2000 Olympic Games": ("2000-09-27", "2000-09-30"),
    "Athens 2004 Olympic Games": ("2004-08-26", "2004-08-29"),
    "Beijing 2008 Olympic Games": ("2008-08-20", "2008-08-23"),
    "London 2012 Olympic Games": ("2012-08-08", "2012-08-11"),
}
for event_name, dates in olympic_date_fixes.items():
    mask = df["event_name"] == event_name
    df.loc[mask, "start_date"] = dates[0]
    df.loc[mask, "end_date"] = dates[1]

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

#removing bugged fights in the data set which only have one fighter
unusable_fights = (
    df["fighter_a"].isna()|
    df["fighter_b"].isna()|
    df["winner"].isna()
    )
df = df[~unusable_fights].copy()
#getting rid of para,junior and cadet fights to leave only the senior divisions
exclude_events = (
    df["event_name"].str.contains("Para", case=False, na=False) |
    df["event_name"].str.contains("Junior", case=False, na=False) |
    df["event_name"].str.contains("Cadet", case=False, na=False) 
)
#getting rid of the childrens fights
boys_girls = df["weight_category"].str.contains(
    "Boys|Girls",
    case = False,
    na = False,
    regex = True
)
df = df[~exclude_events].copy()
df = df[~boys_girls].copy()
#fixing manchester gp 2013 +58 error as should be -58
manchester_58_error = (
    (df["event_name"] == "Manchester 2013 World Taekwondo Grand Prix") &
    (df["weight_category"] == "Men +58kg")
)
df.loc[manchester_58_error, "weight_category"] = "Men -58kg"

#cleaning china open data to remove junior categories
youth_weights_by_event = {
    "2025 China Open International Taekwondo Championships": [
        "Men -45kg",
        "Men -48kg",
        "Men -51kg",
        "Men -55kg",
        "Men -59kg",
        "Men -73kg",
        "Men -78kg",
        "Men +78kg",
        "Women -44kg",
        "Women -55kg",
        "Women -59kg",
        "Women -63kg",
        "Women -68kg",
        "Women +68kg",
    ],

    "European Small States Championships 2025": [
        "Men -45kg",
        "Men -55kg",
        "Men -59kg",
        "Men -73kg",
        "Men -78kg",
        "Women -52kg",
        "Women -55kg",
        "Women -59kg",
        "Women -63kg",
        "Women -68kg",
    ]
}

youth_divisions = pd.Series(False, index=df.index)

for event_name, weights in youth_weights_by_event.items():
    youth_divisions |= (
        (df["event_name"] == event_name) &
        (df["weight_category"].isin(weights))
    )

df = df[~youth_divisions].copy()

#standardizing weight category names
df["weight_category"] = (
    df["weight_category"].str.strip().str.replace(r"\s+", " ", regex=True)
    .str.replace(r"(?i)^men\s*", "Men ", regex=True)
    .str.replace(r"(?i)^women\s*", "Women ", regex=True)
    .str.replace(r"\s*([+-])\s*", r" \1", regex=True)
)
df.to_csv(
    "data/processed/world_taekwondo_fights_clean.csv",
    index=False
)