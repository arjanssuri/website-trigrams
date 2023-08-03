# website-trigrams
Python script that analyzes Wikipedia articles, extracts specific words related to operators, vehicles, and events, and identifies dates from sentences. It also displays frequently occurring trigrams and the top 10 most frequent bigrams in the corpus using nltk, bs4, requests, and datetime libraries.

Functionality
The script fetches articles from multiple Wikipedia URLs, preprocesses the data, and creates a corpus. It then identifies and extracts specific words related to operators, vehicles, and events from the corpus using WordNet synsets.

The script also extracts dates from the sentences and checks for trigrams that occur more than three times in the corpus. Additionally, it displays the top 10 most frequent bigrams found in the text.

Dependencies
The script is written in Python 3.10.11 and requires the following libraries to be installed:

nltk: For natural language processing tasks
bs4: For web scraping with BeautifulSoup
requests: For making HTTP requests to fetch Wikipedia articles
datetime: For working with dates
Usage
Make sure you have Python 3.10.11 installed on your system.
Install the required libraries using pip:
Copy code
pip install nltk bs4 requests
Run the script by executing the following command in the terminal:
Copy code
python capstone.py
The script will analyze the Wikipedia articles, display identified words, dates, trigrams, and the top 10 most frequent bigrams.
Feel free to modify the URLs in the urls list to analyze different Wikipedia articles.




