def gen_contestant_list(conn):
    contestant_list_query = ("SELECT DISTINCT(Contestant) FROM progress")
    contestants_df = conn.query(contestant_list_query)

    contestant_list = []
    for row in contestants_df.itertuples(index=False):
        contestant_list.append(row.Contestant)

    return contestant_list


def gen_contestant_stats(contestant):
    contestant_stats = ("SELECT Contestant, SUM(Wins) as Wins, SUM(Btms) as Btms, COUNT(*) as Episodes "
                        "FROM ("
                            "SELECT "
                                "Contestant, "
                                "CASE WHEN Result = 'WIN' THEN 1 ELSE 0 END AS Wins, "
                                "CASE WHEN Result = 'BTM' OR Result = 'ELIM' THEN 1 ELSE 0 END AS Btms "
                            "FROM progress) "
                        "GROUP BY Contestant "
                        f"HAVING Contestant = '{contestant}' "
                        "ORDER BY SUM(Wins) ")

    return contestant_stats

def gen_contestant_hometowns(season=None):
    if not season:
        hometown_stats = ("SELECT SUBSTR(Hometown, (INSTR(Hometown, ',') + 1), LENGTH(Hometown)) as state, COUNT(*) as Queens "
                          "FROM contestants "
                          "GROUP BY state "
                          "ORDER BY Queens DESC")

    else:
        hometown_stats = (
                        "SELECT SUBSTR(Hometown, (INSTR(Hometown, ',') + 1), LENGTH(Hometown)) as state, COUNT(*) as num "
                        "FROM contestants "
                        "GROUP BY state "
                        "ORDER BY num DESC")

    return hometown_stats

def gen_average_ages():
    age_stats = ("SELECT Season, ROUND(AVG(Age)) as Age " 
                  "FROM contestants " 
                  "GROUP BY Season "
                  "ORDER BY Season")
    
    return age_stats

def gen_winners_vs_wins():
    winner_stats = ("SELECT Wins AS Challenge_Wins, COUNT(*) AS Number_of_Winners "
                    "FROM ("
                        "SELECT Contestant, SUM(win) as Wins "
                        "FROM ("
                                "SELECT "
                                    "p.Contestant, "
                                    "CASE WHEN p.Result = 'WIN' THEN 1 ELSE 0 END AS win, "
                                    "CASE WHEN c.Placement = 1 THEN 'Yes' ELSE 'No' END AS winner "
                                "FROM progress p "
                                "LEFT JOIN contestants c ON p.Contestant = c.Contestant)"
                            "WHERE Winner = 'Yes'"
                            "GROUP BY Contestant)"
                        "GROUP BY Wins "
                        "ORDER BY Wins DESC")

    return winner_stats

def gen_s16_rollercoaster():
    rollercoaster_stats = ( "SELECT * "
                            "FROM ("
                                "SELECT "
                                    "Contestant, "
                                    "CAST(Season AS INTEGER) AS Season, "
                                    "CAST(Episode AS INTEGER) AS Episode, "
                                    "Result, "
                                    "LAG(Result, 1, 0) OVER (PARTITION BY Contestant ORDER BY Episode) AS Prev_Ep_Result "
                                "FROM progress "
                                "ORDER BY Season)"
                            "WHERE (((Result = 'BTM' or Result = 'ELIM') and Prev_Ep_Result = 'WIN') or (Result ='WIN' and Prev_Ep_Result = 'BTM')) and Season = 16 "
                            "ORDER BY Season, Episode"
    )

    return rollercoaster_stats

def gen_win_streaks():
    win_streak_stats = (
        "SELECT COUNT(*) as Streak, Contestant, Season "
        "FROM ("
            "SELECT * "
            "FROM ("
                "SELECT "
                "Contestant, "
                "CAST(Season AS INTEGER) AS Season, "
                "CAST(Episode AS INTEGER) AS Episode, "
                "Result, "
                "ROW_NUMBER() OVER (PARTITION BY Season, Contestant ORDER BY CAST(Episode AS INTEGER)) - "
                "ROW_NUMBER() OVER (PARTITION BY Season, Contestant, Result ORDER BY CAST(Episode AS INTEGER)) AS Row_Diff "
                "FROM progress)"
            "WHERE Result = 'WIN'"
            "ORDER BY Season, Contestant)"
        "GROUP BY Contestant, Row_Diff "
        "HAVING Streak > 1 "
        "ORDER BY Streak DESC, Season"
    )

    return win_streak_stats
