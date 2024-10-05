import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
from typing import List, Dict, Optional
import random

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the CSV file name
CSV_FILE_NAME = 'quotes.csv'

def scrape_goodreads_quotes(page: int = 1) -> List[Dict[str, str]]:
    """Scrape quotes from Goodreads."""
    url = f"https://www.goodreads.com/quotes?page={page}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        quotes = []
        for quote in soup.find_all('div', class_='quoteDetails'):
            text = quote.find('div', class_='quoteText').get_text(strip=True).split('―')[0].strip()
            author = quote.find('span', class_='authorOrTitle').get_text(strip=True)
            
            quotes.append({
                'text': text,
                'author': author
            })
        
        return quotes
    except requests.RequestException as e:
        logging.error(f"Error scraping Goodreads: {e}")
        return []

def store_quotes_to_csv(quotes: List[Dict[str, str]]) -> None:
    """Store quotes in a CSV file."""
    try:
        with open(CSV_FILE_NAME, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for quote in quotes:
                writer.writerow(quote)
        logging.info(f"Stored {len(quotes)} quotes in {CSV_FILE_NAME}.")
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")

def read_quotes_from_csv() -> List[Dict[str, str]]:
    """Read quotes from the CSV file."""
    quotes = []
    try:
        with open(CSV_FILE_NAME, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                quotes.append(row)
        return quotes
    except Exception as e:
        logging.error(f"Error reading from CSV file: {e}")
        return []

def get_random_quote(quotes: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Retrieve a random quote."""
    return random.choice(quotes) if quotes else None

def search_quotes(quotes: List[Dict[str, str]], keyword: str) -> List[Dict[str, str]]:
    """Search quotes by keyword in text or author."""
    return [q for q in quotes if keyword.lower() in q['text'].lower() or keyword.lower() in q['author'].lower()]

def print_quote(quote: Dict[str, str]) -> None:
    """Print a formatted quote."""
    if quote:
        print(f'"{quote["text"]}" - {quote["author"]}')
    else:
        print("No quote found.")

def main():
    all_quotes = []

    # Scrape quotes if CSV file doesn't exist
    try:
        all_quotes = read_quotes_from_csv()
        if not all_quotes:
            raise FileNotFoundError
    except FileNotFoundError:
        for page in range(1, 6):
            quotes = scrape_goodreads_quotes(page)
            if quotes:
                all_quotes.extend(quotes)
                logging.info(f"Scraped quotes from page {page}")
            else:
                logging.warning(f"No quotes found on page {page}")
            time.sleep(5)
        store_quotes_to_csv(all_quotes)

    while True:
        print("\n1. Get random quote")
        print("2. Search quotes")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            quote = get_random_quote(all_quotes)
            print_quote(quote)

        elif choice == '2':
            keyword = input("Enter a keyword or author's name to search: ")
            quotes = search_quotes(all_quotes, keyword)
            if quotes:
                for quote in quotes:
                    print_quote(quote)
                    print("-" * 50)
            else:
                print("No quotes found matching the keyword or author's name.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
    