import requests
from datetime import date, datetime
from time import sleep
import urllib.parse
import configparser

import database.database_operations as db
from database.models import Crossword, Clue

from scraper import scrape_crossword_data

# Initialize the database session
db_session = db.init_db("sqlite:///crossword_database.db")

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['api_keys']['guardian']
API_URL = "https://content.guardianapis.com/crosswords/series/quick"

from_date = date(2019, 1, 1)
to_date = date.today()

def get_crosswords(api_key, from_date, to_date, page=1):
    formatted_from_date = from_date.strftime("%Y-%m-%d")
    formatted_to_date = to_date.strftime("%Y-%m-%d")
    params = {
        "api-key": api_key,
        "from-date": formatted_from_date,
        "to-date": formatted_to_date,
        "page-size": 50,
        "order-by": "oldest",
        "page": page
    }

    print(API_URL+"?"+urllib.parse.urlencode(params))

    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        crossword_data = response.json()
        process_crosswords(crossword_data['response'])
    else:
        print(f"Failed to retrieve crossword data for {formatted_from_date} (Status Code: {response.status_code})")

def process_crosswords(crossword_data):
    # iterate through crossword page urls and scrape crossword data from pages

    for result in crossword_data['results']:
        # check if crossword has already been scraped
        if db.record_exists(db_session, Crossword, result['id']):
            print(f"Skipping record ID {result['id']} because it already exists.")
            continue

        # Convert timestamp to Python datetime object
        timestamp = result['webPublicationDate']
        date_published = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

        # create crossword object
        crossword = Crossword(
          id = result['id'],
          web_title = result['webTitle'],
          web_url = result['webUrl'],
          date_published = date_published
        )

        print(f"Crossword ID: {crossword.id}")

        # now scrape clues from webpage
        clues_list = scrape_crossword_data(result['webUrl'])
        
        # assign clues to crossword object
        crossword.clues = clues_list

        # save to database
        db_session.add(crossword)

        # Commit changes and close the session
        db_session.commit()
        db_session.close()


    if crossword_data['currentPage'] < crossword_data['pages'] :
        page = crossword_data['currentPage'] + 1

        sleep(1) # Rate limit: 1 request per second
        get_crosswords(API_KEY, from_date, to_date, page)
    
if __name__ == "__main__":
    get_crosswords(API_KEY, from_date, to_date)
