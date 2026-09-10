# Rupaul's Drag Race ETL Pipeline
# ✨ [Live Streamlit Demo](https://drag-race-data-project.streamlit.app/)✨ 

<img width="480" height="480" alt="giphy" src="https://github.com/user-attachments/assets/8c0f14f5-b17a-4507-ab03-2054b38689a9" />

Rupaul's Drag Race is a reality tv competition show featuring drag queens competing in challenges to ultimately win the title of America's Next Drag Superstar. 

As someone who loves stats, reality tv, and drag, I knew this show was the perfect source to use for a data pipeline project!

This project contains both a data pipeline, and a Streamlit app performing some data analysis/visualization on the data generated with the pipeline.

## The ETL Pipeline:
- extract.py uses BeautifulSoup, lxml, and pandas to scrape data from the Wikipedia pages of each U.S. season of RuPaul's Drag Race.
- transform.py uses pandas to transform and clean the extracted data.
- load.py uses sqlite3 to load the transformed data into a SQL database
- pipeline.py orchestrates the functions from the 3 previous files together, running the ETL pipeline from start to finish.

## The Streamlit App:
- app.py builds a Streamlit app using the SQL database generated from the pipeline, and creates various data visualizations
- queries.py contains functions returning SQL queries used in the Streamlit app, which are then used by each visualization
  
Click [this link](https://drag-race-data-project.streamlit.app/) to check out the deployed Streamlit app!

<img width="2465" height="1190" alt="Screenshot_9-9-2026_233820_drag-race-data-project streamlit app" src="https://github.com/user-attachments/assets/8eeaf52b-5769-4f46-bd3e-13de6f9ea653" />
(A screenshot of some of the visualizations on the app!)


## Installation
1. Clone the repository
```   
git clone https://github.com/CLEWARNE99/drag_race_data_project.git
```
2. Install dependencies
```
pip install -r requirements.txt
```

## Running the Pipeline
To run the pipeline and generate the database run:
```
python pipeline.py
```
**Note: I have included the .db file in the repository, so that the Streamlit app can read from the database. However, if you run the pipeline it will regenerate the database from scratch.
## Running Streamlit App locally
To run the streamlit app locally, run:
```
streamlit run app.py
```

## Some Reflection
Starting this project out, I was storing data in csv files and then reading those csv files into pandas dataframes. After further research, I realized that skipping the csv step actually makes the pipeline much more concise and the data flows way more simply betweeen each step.

As I was building this pipeline, I thought to myself, what fun is getting all of this data without doing some analysis/visualization with it? This lead me to the idea of building the Streamlit app!

Having taught myself SQL a while back and doing data analysis projects for fun, I found the data analysis/visualization part of this project a comforting return to some of my earlier work! I remember always being so frustrated that I couldn't find many public datasets that I found interesting, so it's so cool to come full circle and know that now, 
I can create datasets to do analysis projects with.

If I were to add anything to this project, I think it would be cool to also add data from Rupaul's Drag Race All-Stars seasons, and international seasons! Looking at queens' journeys from their original seasons, to All-Stars and international seasons could add a fun layer to explore.
