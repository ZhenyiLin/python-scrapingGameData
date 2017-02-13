# Python Web-scraping of Game database #

## Scraping game data from [GameFAQs](https://www.gamefaqs.com)
Scraping data in more than 30 game platforms, which includes: PS, PS2, PS3, PS4, Wii, Wii-U, XBOX, XBOXONE, iPhone, Android, etc. 

### Part I: generate htmls ###
Run 'href_generator_v4.py' to generate game htmls in each platform. The htmls file will be saved under './html/' directory.

### Part II: parse game data ###
Run 'parse_v6.py', which read previous game htmls and scrape and save game data into csv files under './data/' directory.

### The scraped game data ###
Below lists main items in the scraped data:
- Title: game title
- Description: game description
- ReleaseDate: game released data, including new coming game marked as 'TBA'
- Category: game category and subcategories
- Platform: game platform
- PlayTime: the statistics of playTime for each game
- Difficulty: the statistics of difficulty for each game
- Play: the statistics of play progress for each game
- Ownership: the statistics of ownership for each game
- Star: the statistics of user rating for each game (1 - 5 stars)
- Critic: the averaged score of critic reviews for each game
- Reviews: the total number of user reviews for each game 


