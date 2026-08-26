import pandas as pd

def transform_contestant_data(contestant_data):

    df = contestant_data

    #Clean Placement column
    df["Placement"] = df["Placement"].ffill()

    #Remove wikipedia tags
    tag_list = ["[a]","[b]","[c]","[d]","[e]","[f]","[g]", "[h]"]
    for tag in tag_list:
        df["Contestant"] = df["Contestant"].str.replace(pat=tag, repl="")
        df["Age"] = df["Age"].str.replace(pat=tag, repl="")
        df["Hometown"] = df["Hometown"].str.replace(pat=tag, repl="")
        df["Placement"] = df["Placement"].str.replace(pat=tag, repl="")

    #Contestant "Shangela Laquifa Wadley" is listed as just "Shangela" Season 3. Updating
    #Season 2 name for data consistency.
    df["Contestant"] = df["Contestant"].replace({"Shangela Laquifa Wadley": "Shangela"})

    #Make runner-up string consistent
    df["Placement"] = df["Placement"].replace({"Runners-up": "Runner-up"})

    #Translate placement colum vals to numerical values, 0 represents "Disqualified"
    df["Placement"] = df["Placement"].replace({"Winner": "1"})
    df["Placement"] = df["Placement"].replace({"Runner-up": "2"})
    df["Placement"] = df["Placement"].replace({"Disqualified": "0"})
    df["Placement"] = df["Placement"].str.replace("[A-Za-z]", repl="", regex=True)

    #Strip whitespace
    df["Placement"] = df["Placement"].str.strip()

    #Transform data types
    #Transform from string into numerical value for age and placement cols
    df["Season"] = df["Season"].astype(int)
    df["Age"] = df["Age"].astype(int)
    df["Placement"] = df["Placement"].astype(int)

    #print(df.to_string())
    return df

def transform_progress_data(progress_data):
    #df = pd.read_csv("rpdr_progress_data.csv")
    df = progress_data

    #Remove wikipedia tags
    tag_list = ["[a]", "[b]", "[c]", "[d]", "[e]", "[f]", "[g]", "[h]"]
    for tag in tag_list:
        df["Contestant"] = df["Contestant"].str.replace(pat=tag, repl="")
        for num in range(1, 18):
            df[f"{num}"] = df[f"{num}"].str.replace(pat=tag, repl="")

    #Swap columns 1 and 2
    col_2 = df.pop("Contestant")
    df.insert(0, "Contestant", col_2)

    return df
