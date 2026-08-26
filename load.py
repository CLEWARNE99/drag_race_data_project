import sqlite3

def load_to_db(contestant_df, progress_df):
    #Create db
    conn = sqlite3.connect("rpdr_analysis.db")

    #Create tables in db from dfs
    contestant_df.to_sql("contestants", conn, if_exists="replace", index=False)
    progress_df.to_sql("progress", conn, if_exists="replace", index=False)

    conn.close()

    print("Data loaded.")