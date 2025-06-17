# Wikipedia Most Read Articles

This Python project automates the process of retrieving and compiling data about the most read Wikipedia articles over a user-defined date range. It uses web automation to navigate Wikipedia's pageview statistics, changes the display language to English, sets the data view to daily mode, and collects data for each day within the specified period. The project then aggregates the page views of articles appearing multiple times in the top 100 and generates an Excel report summarizing the most popular Wikipedia pages during that timeframe.

## Features

- Prompts the user to input an initial and final date in `dd.mm.yyyy` format.  
- If no dates are provided, the program uses predefined default dates.  
- Opens the Wikipedia "Topviews" statistics page automatically.  
- Changes the language of the page to English for consistent parsing.  
- Sets the data display mode to daily to retrieve daily statistics.  
- Iterates through the specified date range, scraping the top 100 most read articles each day.  
- Aggregates data by summing page views and edits for articles appearing multiple times in the date range.  
- Calculates a ratio of pageviews to number of edits for additional insight.  
- Exports the aggregated data into an Excel file named `wikipedia_page_data.xlsx`.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/savahh27/wikipedia_most_read_articles.git
   cd wikipedia_most_read_articles

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
