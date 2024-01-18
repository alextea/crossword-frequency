import requests
import json
from bs4 import BeautifulSoup

def scrape_crossword_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with the class 'js-crossword' and get the 'data-crossword-data' attribute
        crossword_div = soup.find('div', class_='js-crossword')
        if crossword_div:
            crossword_data_json = crossword_div.get('data-crossword-data')
            
            # Parse the JSON data
            try:
                crossword_data = json.loads(crossword_data_json)
                return crossword_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("Crossword div not found")
            return None
    else:
        print(f"Failed to retrieve page (Status Code: {response.status_code})")
        return None

if __name__ == "__main__":
    crossword_url = "https://www.theguardian.com/crosswords/quick/16755"
    crossword_data = scrape_crossword_data(crossword_url)
    
    if crossword_data:
        print("Crossword Data:")
        print(json.dumps(crossword_data, indent=2))
