# Goodreads Quote Scraper

This project is a Python script that scrapes inspirational quotes from Goodreads, stores them in a CSV file, and provides a simple interface to retrieve and search for quotes.

## Features

- Scrapes quotes from Goodreads
- Stores quotes in a CSV file
- Retrieves random quotes
- Searches quotes by keyword or author's name
- Simple command-line interface

## Requirements

- Python 3.6+
- requests
- beautifulsoup4

## Installation

1. Clone this repository:

2. Install the required packages:

## python main.py

The script will scrape quotes from Goodreads if the CSV file doesn't exist. Then, it will present a menu with the following options:

1. Get a random quote
2. Search quotes
3. Exit

Choose an option by entering the corresponding number.

## CSV File

The scraped quotes are stored in a file named `quotes.csv` in the same directory as the script. Each row in the CSV file contains:

- Quote text
- Author


## Note

This script is for educational purposes only. When using it, please respect Goodreads' resources and terms of service.
