import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime  # Change Date to DateTime
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class CrosswordEntry(Base):
    __tablename__ = 'crossword_entries'

    id = Column(Integer, primary_key=True)
    crossword_id = Column(String)
    clue_number = Column(Integer)
    clue_direction = Column(String)
    clue_text = Column(String)
    solution = Column(String)
    date_published = Column(DateTime)  # Change to DateTime

    def __repr__(self):
        return f"<CrosswordEntry(id={self.id}, crossword_id={self.crossword_id}, clue_number={self.clue_number}, clue_direction={self.clue_direction}, clue_text={self.clue_text}, solution={self.solution}, date_published={self.date_published})>"

def scrape_and_save_to_database(url, database_url="sqlite:///crossword_database.db"):
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

            # Load the JSON data
            crossword_data = json.loads(crossword_data_json)

            # Convert timestamp to Python datetime object
            timestamp = crossword_data['date']
            date_published = datetime.utcfromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds

            # Create the SQLAlchemy engine and bind it to the session
            engine = create_engine(database_url)
            Base.metadata.create_all(engine)
            session = Session(engine)

            # Insert crossword entries into the database
            for entry_data in crossword_data['entries']:
                entry = CrosswordEntry(
                    crossword_id=crossword_data['id'],
                    clue_number=entry_data['number'],
                    clue_direction=entry_data['direction'],
                    clue_text=entry_data['clue'],
                    solution=entry_data['solution'],
                    date_published=date_published
                )
                session.add(entry)

            # Commit changes and close the session
            session.commit()
            session.close()

            print("Data saved to the database successfully.")
                
        else:
            print("Crossword div not found")
    else:
        print(f"Failed to retrieve page (Status Code: {response.status_code})")

if __name__ == "__main__":
    crossword_url = "https://www.theguardian.com/crosswords/quick/16755"
    scrape_and_save_to_database(crossword_url)
