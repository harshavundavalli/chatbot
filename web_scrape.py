import urllib
import re
from urllib import request
from urllib.request import urlopen
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from langdetect import detect
from collections import defaultdict
import string
import pickle




def contains_url_keys(url, url_keys):
    return any(key in url.lower() for key in url_keys)



def crawl(start_urls, max_urls):
    
    crawled_urls = set(start_urls)
    to_crawl = list(start_urls)
    keys=['NTR','harikrishna','kalyan ram','balakrishna','lakshmi pranathi','nandamuri taraka rama rao','N._T._Rama_Rao_Jr',]
    

    # Continue crawling until the list of URLs to crawl is not empty or until we reach the maximum URL limit
    while to_crawl:
        current_url = to_crawl.pop(0)  # Take the first URL from the list to crawl
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                page_text = soup.get_text()
                # Find relevant URLs within the current page
                links = soup.find_all('a', href=True)
            
            
                for link in links:
                    url = link['href']
                    # Check if the URL is an absolute URL and if it hasn't been crawled before
                    if url.startswith('http')  and url not in crawled_urls and contains_url_keys(url,keys) :
                        crawled_urls.add(url)  # Add the URL to the set of crawled URLs
                        to_crawl.append(url)   # Add the URL to the list of URLs to crawl

                    # If we have crawled the maximum number of URLs, exit the loop
                    if len(crawled_urls) >= max_urls:
                        break

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return list(crawled_urls)

def scrape_and_write(urls,output_dir):
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)  # Send a GET request to the URL
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content
            
            text=' '
            paragraphs=soup.find_all('p')
            for para in paragraphs:
                text += para.get_text().lower()
            # Write the extracted text to a file
            filename = os.path.join(output_dir, f"file_{i}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)

        except Exception as e:
            print(f"Error scraping {url}: {e}")



start_urls=['https://en.wikipedia.org/wiki/N._T._Rama_Rao_Jr.','https://en.wikipedia.org/wiki/N._T._Rama_Rao_Jr._filmography','https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_N._T._Rama_Rao_Jr.']
max_urls=15
crawled_urls=crawl(start_urls,max_urls)

print(len(crawled_urls))

output_dir = 'scraped_texts_NTR'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

scrape_and_write(crawled_urls, output_dir)
print("Text scraped and written to files successfully.")

