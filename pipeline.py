from extract import create_contestants_df, create_progress_df
from transform import transform_contestant_data, transform_progress_data
from load import load_to_db

def pipeline():
    #Extract data
    contestants_df = create_contestants_df()
    progress_df = create_progress_df()

    #Transform data
    contestants_cleaned = transform_contestant_data(contestants_df)
    progress_cleaned = transform_progress_data(progress_df)

    #Load data
    load_to_db(contestants_cleaned, progress_cleaned)

if __name__ == "__main__":
    pipeline()