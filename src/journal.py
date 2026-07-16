import sqlite3, json, datetime, os
from turtle import pd
from turtle import pd

DB = os.path.join("data", "journal.db")


def init_db():
         os.makedirs("data", exist_ok=True)
         with sqlite3.connect(DB) as con:
             con.execute("""CREATE TABLE IF NOT EXISTS entries (
                 id INTEGER PRIMARY KEY,
                 ts TEXT,
                 message TEXT,
                 emotions TEXT
             )""")


def log(message: str, emotions: dict):
          with sqlite3.connect(DB) as con:
             con.execute("INSERT INTO entries (ts, message, emotions) VALUES (?,?,?)",
                        (datetime.datetime.now().isoformat(), message,
                         json.dumps(emotions)))


def load_history_df():
          import pandas as pd
          with sqlite3.connect(DB) as con:
             df = pd.read_sql("SELECT * FROM entries", con)
          df["emotions"] = df["emotions"].apply(json.loads)
          return df
