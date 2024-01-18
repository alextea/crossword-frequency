import requests
from bs4 import BeautifulSoup

def scrape_crossword_clues(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the crossword clues from the page
        clues = []
        for clue_elem in soup.select('li.crossword__clue'):
            clue_text = clue_elem.get_text(strip=True)
            clues.append(clue_text)
        
        return clues
    else:
        print(f"Failed to retrieve page (Status Code: {response.status_code})")
        return None

if __name__ == "__main__":
    crossword_url = "https://www.theguardian.com/crosswords/quick/16755"
    crossword_clues = scrape_crossword_clues(crossword_url)
    
    if crossword_clues:
        for i, clue in enumerate(crossword_clues, 1):
            print(f"{i}. {clue}")
