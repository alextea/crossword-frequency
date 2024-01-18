import requests
from bs4 import BeautifulSoup
import json
import sqlite3

def scrape_and_save_to_database(url, database_name="crossword_database.db"):
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
                
                # Connect to the SQLite database
                connection = sqlite3.connect(database_name)
                cursor = connection.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS crossword_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        crossword_id TEXT,
                        clue_number INTEGER,
                        clue_direction TEXT,
                        clue_text TEXT,
                        solution TEXT,
                        date_published INTEGER
                    )
                ''')

                # Insert crossword entries into the database
                for entry in crossword_data['entries']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO crossword_entries 
                        (crossword_id, clue_number, clue_direction, clue_text, solution, date_published)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        crossword_data['id'],
                        entry['number'],
                        entry['direction'],
                        entry['clue'],
                        entry['solution'],
                        crossword_data['date'],
                    ))

                # Commit changes and close the connection
                connection.commit()
                connection.close()

                print("Data saved to the database successfully.")
                
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("Crossword div not found")
    else:
        print(f"Failed to retrieve page (Status Code: {response.status_code})")

if __name__ == "__main__":
    crossword_url = "https://www.theguardian.com/crosswords/quick/16755"
    scrape_and_save_to_database(crossword_url)
