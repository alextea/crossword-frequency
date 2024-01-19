import requests
from datetime import date
from time import sleep
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['api_keys']['guardian']
API_URL = "https://content.guardianapis.com/crosswords/series/quick"

from_date = date(2019, 1, 1)
to_date = date.today()

crossword_urls = []

def get_crossword_data(api_key, from_date, to_date, page=1):
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
        process_crossword_data(crossword_data['response'])
    else:
        print(f"Failed to retrieve crossword data for {formatted_from_date} (Status Code: {response.status_code})")

def process_crossword_data(crossword_data):
    # Implement logic to process and save crossword data as needed
    # You can adapt the previous code to save crossword data to the database
    # print(json.dumps(crossword_data, indent=2))
    for result in crossword_data['results']:
        crossword_urls.append(result['apiUrl'])

    if crossword_data['currentPage'] < crossword_data['pages'] :
        api_key = API_KEY
        page = crossword_data['currentPage'] + 1

        sleep(1) # Rate limit: 1 request per second
        get_crossword_data(api_key, from_date, to_date, page)
    else:
        print("\n".join(crossword_urls)) 
    


if __name__ == "__main__":
    api_key = API_KEY

    get_crossword_data(api_key, from_date, to_date)
