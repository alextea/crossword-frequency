import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

from database.database_operations import init_db
from database.models import Crossword, Clue

# Initialize the database session
db_session = init_db("sqlite:///crossword_database.db")

def scrape_crossword_data(url, database_url="sqlite:///crossword_database.db"):
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

if __name__ == "__main__":
    pass