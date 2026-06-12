from bs4 import BeautifulSoup
import requests
import lxml
import time
import csv

def scrape_contestants(season_number):
    """
    Takes RPDR season number, and scrapes Wikipedia page for Contestants table.
    """

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
    for tr in contestants_table.find_all("tr"):
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

#Initialize list to hold data that will be used to write csv.
season_data = []

#Scrape data for each season.
for season in range (1,19):
    season_data.append(scrape_contestants(season)[1])

    #Sleep as courtesy.
    time.sleep(1)

#Create or overwrite csv file with scraped data.
with open("rpdr_contestant_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    #Add header row.
    writer.writerow(["Season", "Contestant", "Age", "Hometown", "Placement"])

    for season in season_data:
        for data_row in season:
            writer.writerow(data_row)