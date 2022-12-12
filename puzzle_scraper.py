import requests
from pathlib import Path
import browser_cookie3
import datetime as dt
import json

# This script will scrape the puzzle input from the Advent of Code website
# and save it to a file in the inputs folder.
# It will also save a HTML copy of the puzzle page to the inputs folder.

config = json.load(open("config.json", "r"))

if "cookie_file" not in config:
    config["cookie_file"] = "C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Network\\Cookies"

class PuzzleScraper:
    def __init__(self, year, day):
        self.year = year
        self.day = day
        self.session_cookie = browser_cookie3.chrome(
            domain_name=".adventofcode.com",
            cookie_file=config["cookie_file"],
        )
        self.puzzle_page_url = f"https://adventofcode.com/{year}/day/{day}"
        self.puzzle_input_url = f"https://adventofcode.com/{year}/day/{day}/input"
        self.puzzle_page_file = Path(f"inputs/{year}/day{day}.html")
        self.puzzle_input_file = Path(f"inputs/{year}/day{day}.txt")
        if not self.puzzle_page_file.parent.exists():
            self.puzzle_page_file.parent.mkdir(parents=True)
        if not self.puzzle_input_file.parent.exists():
            self.puzzle_input_file.parent.mkdir(parents=True)

    def scrape_puzzle_page(self):
        # Make the request to the puzzle page
        r = requests.get(self.puzzle_page_url)
        with open(self.puzzle_page_file, "wb+") as f:
            f.write(r.content)
        return r

    def scrape_puzzle_input(self):
        # Make the request to the puzzle input
        # this requires some trickery as the input is not available until we sign in
        # so we need to use the session cookie from our google chrome browser
        r = requests.get(self.puzzle_input_url, cookies=self.session_cookie)
        # Save the puzzle input to a file
        with open(self.puzzle_input_file, "w") as f:
            f.write(r.text)
        # Return the puzzle input
        return r.text


if __name__ == "__main__":
    year = dt.datetime.now().year
    day = dt.datetime.now().day
    # lets also check if all the previous days have been completed
    for d in range(1, day + 1):
        # use asyncio to delay the requests and avoid spamming the server
        scraper = PuzzleScraper(year, d)
        if not scraper.puzzle_input_file.exists():
            print(f"Input file {scraper.puzzle_input_file} does not exist.")
            # Scrape the puzzle
            puzzle_input = scraper.scrape_puzzle_input()
            print(f"Scraped puzzle input for day {d}: {puzzle_input}")
        else:
            print(f"Input file {scraper.puzzle_input_file} already exists.")
        if not scraper.puzzle_page_file.exists():
            print(f"HTML file {scraper.puzzle_page_file} does not exist.")
            puzzle_page = scraper.scrape_puzzle_page()
            print(f"Scraped puzzle page for day {d}: {puzzle_page}")
        else:
            print(f"HTML file {scraper.puzzle_page_file} already exists.")
