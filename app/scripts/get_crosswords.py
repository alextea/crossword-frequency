import requests
from bs4 import BeautifulSoup
import json
from datetime import date, datetime
from time import sleep
import urllib.parse
from flask.cli import AppGroup
from flask import current_app as app

from app.database import database_operations as db
from app.database.models import Crossword, Clue


from_date = date(2019, 1, 1)
to_date = date.today()

db_cli = AppGroup('database')

@db_cli.command("populate")
def populate():
    api_key = app.config['GUARDIAN_API_KEY']

    page = 1
    crossword_data = get_and_process_crosswords(api_key, from_date, to_date, page)
    
    while crossword_data['currentPage'] < crossword_data['pages'] :
        page = crossword_data['currentPage'] + 1

        sleep(1) # Rate limit: 1 request per second
        crossword_data = get_and_process_crosswords(api_key, from_date, to_date, page)

def get_and_process_crosswords(api_key, from_date, to_date, page):
    crossword_data = get_crosswords(api_key, from_date, to_date, page)
    process_crosswords(crossword_data)
    return crossword_data

def get_crosswords(api_key, from_date, to_date, page=1):
    api_url = "https://content.guardianapis.com/crosswords/series/quick"
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

    print(api_url+"?"+urllib.parse.urlencode(params))

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        crossword_data = response.json()
        return crossword_data['response']
    else:
        print(f"Failed to retrieve crossword data for {formatted_from_date} (Status Code: {response.status_code})")

def process_crosswords(crossword_data):
    # iterate through crossword page urls and scrape crossword data from pages

    # Initialize the database session
    db_session = db.init_db(app.config['SQLALCHEMY_DATABASE_URI'])

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

        sleep(1) # Rate limit: 1 request per second
    
def scrape_crossword_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    clues_list = []
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with the class 'js-crossword' and get the 'data-crossword-data' attribute
        crossword_div = soup.find('div', class_='js-crossword')
        if crossword_div:
            crossword_data_json = crossword_div.get('data-crossword-data')

            # Load the JSON data
            crossword_data = json.loads(crossword_data_json)

            # create clue objects from json
            for entry_data in crossword_data['entries']:
                entry = Clue(
                    crossword_id=crossword_data['id'],
                    clue_number=entry_data['number'],
                    clue_direction=entry_data['direction'],
                    clue_text=entry_data['clue'],
                    solution=entry_data['solution'],
                )

                print(f"Solution: {entry.solution}")

                clues_list.append(entry)
            
            return clues_list
        else:
            print("Crossword div not found")
    else:
        print(f"Failed to retrieve page (Status Code: {response.status_code})")

