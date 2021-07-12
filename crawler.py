import urllib.request
import os
import time
import threading
from bs4 import BeautifulSoup

# number of web pages saved
MAX_DOCUMENTS = 10
# minimum number of words
WORDS_MINIMUM = 200

search_terms = ["facebook", "tiktok", "twitter"]
page_delimiter = "&start={}"

# user agent string
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

# check word count on articles by counting words surrounded by paragraph tags
def word_count(url):
    request = urllib.request.Request(url, headers=header)

    # may crash if website returns error
    try:
        page = urllib.request.urlopen(request, timeout=2)
    
        # lxml - html/ xml processor
        soup = BeautifulSoup(page, "lxml")

        # word count
        words_count = 0

        # find the <p> tags
        for info in soup.find_all("p"):
            words_count += len(info.get_text().split())
        
    except:
        print("Error with webpage!\n")
        return 0
    
    return words_count

# parse a webpage, if suitable, save as html file
def parse_webpage(target_function):
    threads = []

    for term in search_terms:
        thread = threading.Thread(target=target_function, args=(term,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# regular google search results, but gives results such as youtube, etc
def google_search(term):

    results = 0
    current_page = 1

    # make directory for search results
    directory = os.path.join(os.getcwd(), "Dataset", term.replace(" ", "_"))
    os.mkdir(directory)

    # keep going through google results until we have correct number of documents
    while results < MAX_DOCUMENTS:
        url = "https://www.google.com/search?q=" + term.replace(" ", "+") + page_delimiter.format(current_page * 10)
        request = urllib.request.Request(url, headers=header)
        page = urllib.request.urlopen(request)
        # lxml - html/ xml processor
        soup = BeautifulSoup(page, "lxml")
        # finds all the headers from google search
        for info in soup.find_all("h3"):
            # check that header belongs to an anchor
            if info.parent.name == "a":
                url = info.parent["href"]

                # check word count, if under, skip website
                words = word_count(url)

                if (words < WORDS_MINIMUM):
                    print("header " + info.text + "\nurl " + url + "\nword count < " + str(WORDS_MINIMUM) + " skipping..." + "\n")
                    continue
                else:
                    print("header " + info.text + "\nurl " + url + "\nword count " + str(words) + "\n")
                    results += 1

                # use try/catch since some websites may 403
                try:
                    # save to file
                    request = urllib.request.Request(url, headers=header)
                    search_result = urllib.request.urlopen(request)
                    fp = open(os.path.join(directory, "articles{}.html".format(results)), "wb")
                    fp.write(search_result.read())
                    fp.close()
                except:
                    print("error when writing file, skipping\n")
                    results -= 1
                # check if we have enough results
                if results == MAX_DOCUMENTS:
                    break

        if results == MAX_DOCUMENTS:
            break
        current_page += 1

def google_news_search(term):
    
    attributes = {"role": "heading"}

    results = 0
    current_page = 1

    # make directory for search results
    directory = os.path.join(os.getcwd(), "Dataset", term.replace(" ", "_"))
    os.mkdir(directory)
    
    # keep going through google news results until we have correct number of documents
    while results < MAX_DOCUMENTS:
        url = "https://www.google.com/search?q=" + term.replace(" ", "+") + page_delimiter.format(current_page * 10) + "&tbm=nws"
        request = urllib.request.Request(url, headers=header)
        page = urllib.request.urlopen(request)
        # lxml - html/ xml processor
        soup = BeautifulSoup(page, "lxml")
        # find the div with the news article
        for info in soup.find_all("div", attributes):
            # check that header belongs to an anchor
            if info.parent.parent.parent.name == "a":
                url = info.parent.parent.parent["href"]
                
                # check word count, if under, skip website
                words = word_count(url)

                if (words < WORDS_MINIMUM):
                    print("header " + info.text + "\nurl " + url + "\nword count < " + str(WORDS_MINIMUM) + " skipping..." + "\n")
                    continue
                else:
                    print("header " + info.text + "\nurl " + url + "\nword count " + str(words) + "\n")
                    results += 1
                # use try/catch since some websites may 403
                try:
                    # save to file
                    request = urllib.request.Request(url, headers=header)
                    search_result = urllib.request.urlopen(request)
                    fp = open(os.path.join(directory, "articles{}.html".format(results)), "wb")
                    fp.write(search_result.read())
                    fp.close()
                except:
                    print("error when writing file, skipping\n")
                    results -= 1
                # check if we have enough results
                if results == MAX_DOCUMENTS:
                    break

        if results == MAX_DOCUMENTS:
            break
        current_page += 1

def main():
    # start time
    start = time.time()

    parse_webpage(google_news_search)

    # end time
    end = time.time()

    print("Elapsed time: {:.2f} seconds".format(end - start))

if __name__ == "__main__":
    main()