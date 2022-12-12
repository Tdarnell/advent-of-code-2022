from pathlib import Path
from puzzle_scraper import PuzzleScraper
import datetime as dt

def get_input(day: int, year: int = 2022):
    input_file = Path(f"inputs/{year}/day{day}.txt")
    if not input_file.exists():
        print(
            f"[Utils]: Input file {input_file} does not exist, attempting to scrape it."
        )
        try:
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
        except Exception as e:
            print(f"[Utils]: Failed to scrape input file {input_file}")
            raise e
    # Assert that the file exists one last time
    if not input_file.exists():
        raise FileNotFoundError(f"[Utils] Input file {input_file} does not exist.")
    return input_file
        