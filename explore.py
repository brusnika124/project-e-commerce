from pathlib import Path

import pandas as pd

project_dir = Path(__file__).resolve().parent
file_path = project_dir / "data" / "raw" / "events.csv"
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.width', 200)
events = pd.read_csv(file_path)
events["event_datetime"] = pd.to_datetime(
    events["timestamp"],
    unit="ms",
    utc=True,
)
events = events.drop(columns=["timestamp"])
duplicate_mask = events.duplicated()
rows_before = len(events)
events = events.drop_duplicates(ignore_index=True)
check = pd.crosstab(events["event"], events["transactionid"].notna())
purchase_events = events[events["event"] == "transaction"]
visitors = events["visitorid"].nunique()
buyers = purchase_events["visitorid"].nunique()
transactions = purchase_events["transactionid"].nunique()
users_by_event = events.groupby("event")["visitorid"].nunique()
view_ids = events.loc[events["event"] == "view", "visitorid"]
cart_ids = events.loc[events["event"] == "addtocart", "visitorid"]
buyer_ids = purchase_events["visitorid"].drop_duplicates()
events = events.sort_values(["visitorid", "event_datetime"]).reset_index(drop=True)
gap = events.groupby("visitorid")["event_datetime"].diff()
new_session = gap.isna() | (gap >= pd.Timedelta(minutes=30))
events["session_id"] = new_session.cumsum()

sessions = events.groupby("session_id").agg(
    visitorid=("visitorid", "first"),
    session_start=("event_datetime", "min"),
    session_end=("event_datetime", "max"),
    event_count=("event", "size"),
).reset_index()
event_counts = pd.crosstab(events["session_id"], events["event"])
sessions = sessions.join(event_counts, on="session_id")

print(sessions[["view", "addtocart", "transaction"]].gt(0).sum())

print(sessions.head().to_string(index=False))