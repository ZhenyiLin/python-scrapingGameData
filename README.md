# Python Web-scraping of Game database #

## Scraping game data from [GameFAQs](www.gamefaqs.com) ## 
scraping data in more than 30 game platforms, which includes: PS, PS2, PS3, PS4, Wii, Wii-U, XBOX, XBOXONE, iPhone, Android, etc. 

### Part I: generate htmls
run 'href_generator_v4.py' to generate game htmls in each platform.

### Part II: parse game data
run 'parse_v6.py', which read previous game htmls and scrape data, save game data into csv file

### The game database
One downloadable data file is included in '/data/all_data.csv'.   
Below lists main items in the database:
- title: game title
- description: game description
- releaseDate: game released data, including new coming game marked as 'TBA'
- category: game category and subcategories
- platform: game platform
- playTime: the statistics of playTime for each game
- difficulty: the statistics of difficulty for each game
- play: the statistics of play progress for each game
- ownership: the statistics of ownership for each game
- star: the statistics of user rating for each game (1 - 5 stars)
- critic: the averaged score of critic reviews for each game
- reviews: the total number of user reviews for each game 


