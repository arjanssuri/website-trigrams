#################################################################################
#         FILE:
#           assignment5.py
#       AUTHOR:
#           Arjan Suri
#  DESCRIPTION:
#           Assignment 4
#           Opens dataset, preprocesses data, checks top ten most frequent bigrams, and trigrams with more than 3 instances. 
#           Finds specific words and extracts dates
# DEPENDENCIES:
#           Created with Python 3.10.11 (Python version)
#           Created with nltk, bs4 , requests, collections/counter
#################################################################################

from nltk import word_tokenize, sent_tokenize, pos_tag, bigrams
from nltk.corpus import wordnet as wn
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re


from nltk import word_tokenize, sent_tokenize, bigrams, trigrams, FreqDist, pos_tag
from nltk.corpus import wordnet as wn
import re
import requests
from bs4 import BeautifulSoup
import datetime

# Functions for date extraction

def extract_dates(sentence):
    all_dates_from_sentence = set()

    months = ["Jan ","January","Jan."," jan ",'january',

        "Feb ","February","Feb.", 'february',' feb ',

        "Mar ","March","Mar.","march", ' mar ',

        "Apr ","April","Apr.", 'april', ' apr ',

        "May ",

        "Jun ","June","Jun.", 'june', ' jun ',

        "Jul ","July","Jul.", ' july ',' jul ',

        "Aug ","August","Aug.", 'august', 'aug ',

        "Sep ","September","Sep.","Sept.","Sept ", ' sept ','september', ' sep ',

        "Oct ","October","Oct.", ' oct ', 'october',

        "Nov ","November","Nov.",'november', ' nov ',

        "Dec ","December","Dec.", 'december', ' dec ']
    
    for month in months:
        date_list = re.findall(month[0] + r" \d{1,2}(?: \d{4})?", sentence)
        for date in date_list:
            try:
                date_obj = datetime.datetime.strptime(date, '%b %d %Y').date()
                all_dates_from_sentence.add(date_obj.isoformat())
            except ValueError:
                pass

    return all_dates_from_sentence

# Fetch articles from Wikipedia and create the corpus

def fetch_articles(urls):
    corpus = []

    for url in urls:
        response = requests.get(url)
        raw_html = response.text
        raw_html = re.sub(r"\n", " ", raw_html)
        soup = BeautifulSoup(raw_html, "html.parser")
        paragraphs = soup.findAll("p")
        for paragraph in paragraphs:
            text = paragraph.text.lower()
            text = re.sub(r"\[\d+\]", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            corpus.append(text)

    return corpus

# Main function for analyzing the corpus

def analyze_corpus(corpus):
    operator_synset = wn.synset("operator.n.02")
    operate_synset = wn.synset("operate.v.03")
    vehicle_synset = wn.synset("vehicle.n.01")
    event_synset = wn.synset("event.n.01")
    occur_synset = wn.synset("occur.v.01")
    act_synset = wn.synset("act.v.01")

    all_trigrams = trigrams(word_tokenize(' '.join(corpus)))
    trigram_freq_dist = FreqDist(all_trigrams)
    search_trigrams = []
    sentence_count = 0

    for sentence in corpus:
        found_words = [set(), set(), set(), set(), set(), set(), None]
        words = word_tokenize(sentence)
        pos_tagged_words = pos_tag(words)
        match = False

        for (word, pos) in pos_tagged_words:
            if pos.startswith("N") or pos.startswith("V"):
                synsets = wn.synsets(word)
                for synset in synsets:
                    paths = synset.hypernym_paths()
                    for path in paths:
                        if operator_synset in path and pos.startswith("N"):
                            found_words[0].add((word, pos, words.index(word)))
                        if operate_synset in path and pos.startswith("V"):
                            found_words[1].add((word, pos, words.index(word)))
                        if vehicle_synset in path and pos.startswith("N"):
                            found_words[2].add((word, pos, words.index(word)))
                        if event_synset in path and pos.startswith("N"):
                            found_words[3].add((word, pos, words.index(word)))
                        if occur_synset in path and pos.startswith("V"):
                            found_words[4].add((word, pos, words.index(word)))
                        if act_synset in path and pos.startswith("V"):
                            found_words[5].add((word, pos, words.index(word)))

        found_words[6] = extract_dates(sentence)

        if found_words[0] and found_words[1] and found_words[2]:
            min_diff = float('inf')
            min_diff_pair = None

            for (word, pos, index) in found_words[0]:
                for (word2, pos2, index2) in found_words[1]:
                    if index < index2:
                        for (word3, pos3, index3) in found_words[2]:
                            if index2 < index3:
                                diff = index3 - index
                                if diff < min_diff:
                                    min_diff = diff
                                    min_diff_pair = ((word, pos), (word2, pos2), (word3, pos3))

            if min_diff_pair:
                match = True
                print("VEHICLE:", sentence)
                for (word, pos) in min_diff_pair:
                    print(f"\t{pos}: {word}")

        if found_words[3] and (found_words[4] or found_words[5]) and found_words[6]:
            min_diff1 = float('inf')
            min_diff_pair1 = None
            min_diff2 = float('inf')
            min_diff_pair2 = None

            if found_words[4]:
                for (word, pos, index) in found_words[3]:
                    for (word2, pos2, index2) in found_words[4]:
                        if index < index2:
                            diff = index2 - index
                            if diff < min_diff1:
                                min_diff1 = diff
                                min_diff_pair1 = ((word, pos), (word2, pos2))

            if found_words[5]:
                for (word, pos, index) in found_words[3]:
                    for (word2, pos2, index2) in found_words[5]:
                        if index < index2:
                            diff = index2 - index
                            if diff < min_diff2:
                                min_diff2 = diff
                                min_diff_pair2 = ((word, pos), (word2, pos2))

            if min_diff_pair1 or min_diff_pair2:
                match = True
                print("EVENT:", sentence)

                if min_diff1 < min_diff2:
                    for (word, pos) in min_diff_pair1:
                        print(f"\t{pos}: {word}")
                else:
                    for (word, pos) in min_diff_pair2:
                        print(f"\t{pos}: {word}")

                print("\tDates:")
                for date in found_words[6]:
                    print("\t\t", date)

        if match:
            trigrams_sentence = trigrams(words)
            for trig in trigrams_sentence:
                search_trigrams.append(trig)
            sentence_count += 1

    print("Total number of sentences found:", sentence_count)
    print("\nTrigrams from the sentences found that occur at least 3 times in the wider corpus:\n")
    for trig in search_trigrams:
        if trigram_freq_dist[trig] >= 3:
            print(trig)

    bigrams_all = bigrams(word_tokenize(' '.join(corpus)))
    bigram_freq_dist = FreqDist(bigrams_all)
    bigram_freq_dist = sorted(bigram_freq_dist.items(), key=lambda item: item[1], reverse=True)

    print("\nThe top 10 most frequent bigrams:\n")
    for item, freq in bigram_freq_dist[:10]:
        print(item, freq)

# Main program execution

def main():
    urls = ["https://en.wikipedia.org/wiki/Airplane",
            "https://en.wikipedia.org/wiki/Train",
            "https://en.wikipedia.org/wiki/Pilot",
            "https://en.wikipedia.org/wiki/Movie",
            "https://en.wikipedia.org/wiki/Actor",
            "https://en.wikipedia.org/wiki/Ocean%27s_Eleven"
            ]

    corpus = fetch_articles(urls)
    analyze_corpus(corpus)

if __name__ == "__main__":
    main()

