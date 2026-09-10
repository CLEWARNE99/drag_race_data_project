from bs4 import BeautifulSoup
import requests
import lxml
import time
import pandas as pd
from requests import session


def scrape_contestants(season_number):
    """
    Takes RPDR season number, and scrapes Wikipedia page for Contestants table.
    """
    print(f"Scraping contestants, season {season_number}")
    #Create user_agent per Wikipedia bot policy.
    user_agent = {"User-Agent": "Drag_Race_Scraping_Test/1.0 (github.com/CLEWARNE99)"}

    #url to use for scraping with changeable season_number part of url for iteration.
    url = f"https://en.wikipedia.org/wiki/RuPaul's_Drag_Race_season_{season_number}"

    #html text from the request.
    html_text = requests.get(url, headers=user_agent).text

    soup = BeautifulSoup(html_text, "lxml")

    #Find all tables on page.
    tables = soup.find_all("table")

    #Initialize contestants table, and progress table.
    contestants_table = None

    #Initialize caption list to use for filtering through tables.
    caption_list = []

    for table in tables:
        caption = table.find("caption")
        try:
            caption_list.append(caption.text)
        except AttributeError:
            continue

        #Identify contestants table via caption.
        try:
            if "their backgrounds" in caption.text:
                contestants_table = table
        except AttributeError:
            continue

    #Initialize columns and rows for output.
    contestant_cols = []
    contestant_rows = []

    #Initializes names list to append to data rows.
    contestant_names = []

    #Get columns to list.
    for th in contestants_table.find_all("th", scope="col"):
        col_title = th.get_text(strip=True)
        contestant_cols.append(col_title)

    #Get contestant names to list.
    for th in contestants_table.select("th:first-child:not([scope='col'])"):
        contestant = th.get_text(strip=True)
        contestant_names.append(contestant)

    #Get rows to list.
    for tr in contestants_table.select("tr:not([class='mw-empty-elt'])"):
        cr_cells = []
        for td in tr.find_all("td"):
            cr_cells.append(td.get_text(strip=True))
        contestant_rows.append(cr_cells)

    #First row is empty, remove.
    contestant_rows.pop(0)

    #Loop through each row and add contestant name to data in row.
    index = 0
    for row in contestant_rows:
        row.insert(0, contestant_names[index])
        index += 1

    #Loop through each row and add season number to data in row.
    for row in contestant_rows:
        row.insert(0, f"{season_number}")

    return contestant_cols, contestant_rows


def scrape_contestants_all_seasons():
    """
    Returns scraped contestant data for each season.
    """
    # Initialize list to hold data that will be used to write csv.
    contestant_data = []

    #Scrape data for each season.
    for season in range (1,19):
        contestant_data.append(scrape_contestants(season)[1])

        #Sleep as courtesy.
        time.sleep(1)

    return contestant_data

def create_contestants_df():
    """
    Creates DataFrame with scraped contestant data.
    """
    print("Extracting contestant data...")

    contestant_data = scrape_contestants_all_seasons()
    df = pd.DataFrame(columns=("Season", "Contestant", "Age", "Hometown", "Placement"))
    for season in contestant_data:
        new_row = pd.DataFrame(season, columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)

    return df

def scrape_progress(season_number):
    """
    Takes season number, and scrapes progress data from that season.
    """

    print(f"Scraping contestant progress, season {season_number}")

    # Create user_agent per Wikipedia bot policy.
    user_agent = {"User-Agent": "Drag_Race_Scraping_Test/1.0 (github.com/CLEWARNE99)"}

    # url to use for scraping with changeable season_number part of url for iteration.
    url = f"https://en.wikipedia.org/wiki/RuPaul's_Drag_Race_season_{season_number}"

    # html text from the request.
    html_text = requests.get(url, headers=user_agent).text

    soup = BeautifulSoup(html_text, "lxml")

    # Find all tables on page.
    tables = soup.find_all("table")

    # Initialize contestants table, and progress table.
    progress_table = None

    # Initialize caption list to use for filtering through tables.
    caption_list = []

    for table in tables:
        caption = table.find("caption")
        try:
            caption_list.append(caption.text)
        except AttributeError:
            continue

        #Identify progress table via caption.
        try:
            if "progress" in caption.text or "Progress" in caption.text:
                progress_table = table
        except AttributeError:
            continue

        if progress_table is not None:
            break

    progress_cols = []
    progress_rows = []

    contestant_names = []

    if season_number == 10:
        #Season 10's page has rows and columns switched in table.
        for th in progress_table.select("th:first-child:not([scope='row'])"):
            contestant = th.get_text(strip=True)
            if contestant != "Contestant":
                contestant_names.append(contestant)

    else:
        for th in progress_table.select("th:first-child:not([scope='col'])"):
            contestant = th.get_text(strip=True)
            #Season 7 has episodes listed as rows instead of columns, so removing first-child of episodes row.
            if contestant != "1[3]":
                contestant_names.append(contestant)

    for tr in progress_table.find_all("tr"):
        cr_cells = []
        for td in tr.find_all("td"):
            if td.get_text(strip=True):
                cr_cells.append(td.get_text(strip=True))
            else:
                try:
                    for num in range(int(td.get("colspan"))):
                        cr_cells.append("")
                except TypeError:
                    cr_cells.append("")
                except ValueError:
                    for num in range(int(td.get("colspan")[0:2])):
                        cr_cells.append("")
        progress_rows.append(cr_cells)


    progress_rows.pop(0)
    progress_rows.pop(0)

    index = 0
    for row in progress_rows:
        row.insert(0, contestant_names[index])
        index += 1

    for row in progress_rows:
        row.insert(0, f"{season_number}")

    return progress_rows

def scrape_progress_all_seasons():
    """
    Returns scraped progress data from each season.
    """
    # Initialize list to hold data that will be used to write csv.
    progress_data = []

    # Scrape data for each season.
    for season in range(1, 19):
        progress_data.append(scrape_progress(season))

        # Sleep as courtesy.
        time.sleep(1)

    return progress_data

def create_progress_df():
    """
    Creates DataFrame with scraped progress data from each season.
    """

    print("Extracting progress data...")

    progress_data = scrape_progress_all_seasons()
    header_row = []
    header_row.append("Season")
    header_row.append("Contestant")
    for num in range(1, 17):
        header_row.append(f"{num}")
    #Account for split column for Season 16's Sapphira Cristal. Will clean in transform file.
    header_row.append("17")

    header_tuple = ()
    for col in header_row:
        header_tuple += (f"{col}",)

    df = pd.DataFrame(columns=header_tuple)

    for season in progress_data:
        for prog_row in season:
            if len(prog_row) < len(header_tuple):
                len_diff = len(header_tuple) - len(prog_row)
                for i in range(len_diff):
                    prog_row.append("")

        new_row = pd.DataFrame(season, columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)

    return df