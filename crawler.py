import urllib.request
import os
from bs4 import BeautifulSoup

# number of web pages saved
MAX_DOCUMENTS = 10

search_terms = ["facebook", "tiktok", "twitter"]
page_delimiter = "&start={}"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

# regular google search results, but gives results such as youtube, etc
def google_search():
    for term in search_terms:
        results = 0
        current_page = 1

        # make directory for search results
        directory = os.getcwd() + "\\Dataset\\" + term.replace(" ", "_")
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
                    print("header " + info.text)
                    print("url " + url)
                    print()
                    results += 1
                    # use try/catch since some websites may 403
                    try:
                        # save to file
                        search_result = urllib.request.urlopen(url)
                        fp = open("{}\\article{}.html".format(directory, results), "wb")
                        fp.write(search_result.read())
                        fp.close()
                    except:
                        print("error when writing file, skipping")
                        print()
                        results -= 1
                    # check if we have enough results
                    if results == MAX_DOCUMENTS:
                        break

            if results == MAX_DOCUMENTS:
                break
            current_page += 1

def google_news_search():
    
    attributes = {"role": "heading"}

    for term in search_terms:
        results = 0
        current_page = 1

        # make directory for search results
        directory = os.getcwd() + "\\Dataset\\" + term.replace(" ", "_")
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
                    print("header " + info.text)
                    print("url " + url)
                    print()
                    results += 1
                    # use try/catch since some websites may 403
                    try:
                        # save to file
                        search_result = urllib.request.urlopen(url)
                        fp = open("{}\\article{}.html".format(directory, results), "wb")
                        fp.write(search_result.read())
                        fp.close()
                    except:
                        print("error when writing file, skipping")
                        print()
                        results -= 1
                    # check if we have enough results
                    if results == MAX_DOCUMENTS:
                        break

            if results == MAX_DOCUMENTS:
                break
            current_page += 1

def main():
    # google_search()
    google_news_search()

main()