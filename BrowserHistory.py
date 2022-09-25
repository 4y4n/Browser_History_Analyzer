import os
import sqlite3  # sql database library used for fetching browser history data
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt  # to plot data


# This function parses each url so that the returned string is simply the website name and domain
def parse(urls):
    try:
        parsed_url_components = urls.split('//')  # Removed everything left of https://
        sublevel_split = parsed_url_components[1].split('/', 1)  # Removes queries and extra url components
        domain = sublevel_split[0].replace("www.", "")  # Removes www
        return domain
    except IndexError:
        print("URL format error!")


def analyze(results, input_prompt, plot_top=10):
    if input_prompt == "c":
        # Iterates through ordered dictionary and prints each url with the count 
        for site, visits in sites_count_sorted.items():
            print(site, visits)
    else:  
        x = len(sites_count_sorted)
        # Iterates through reverse ordered dictionary and only keeps the last 10 elements
        for site, visits in dict(sites_count_sorted).items():
            x -= 1
            if x >= plot_top:
                del sites_count_sorted[site]
        # Plots the Data using matplotlib
        plt.barh(list(results.keys()), list(results.values()))
        # Adds names of urls and counts to bar graph
        for site, visits in dict(sites_count_sorted).items():
            plt.text(visits, site, visits)
        plt.show()


dataPath = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"  # Default chrome data path
files = os.listdir(dataPath)
historyDB = os.path.join(dataPath, 'history')  # Files in chrome's history folder

c = sqlite3.connect(historyDB)
cursor = c.cursor()
# sql query to accessing urls, and visit counts from the url and visit tables
selectStatement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(selectStatement)  # Requests the library to fetch the urls and visits data with the histroy path
result = cursor.fetchall()  # Data is stored in lists with each url and count stored in sublists
times = []


sites_count = {}
# Iterates through each sublist in results and counts how many times each website has gone through
for url, count in result:
    url = parse(url)  # Parses given url
    if url in sites_count:
        sites_count[url] += 1  # Adds 1 to count if the url has been accessed already
    else:
        sites_count[url] = 1  # Sets count to 1 if website has not been accessed yet

prompt = "yes"
# Input to either plot top 10 websites or print websites
while prompt != "c" and prompt != "p": 
    prompt = str(input("[.] Type < c > to print or < p > to plot \n[>] "))
if prompt == "c":
    # Puts list into ordered disctionary then sorts them by amount of times accessed
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True)) 
else:
    # Puts list into ordered disctionary then sorts them in reversed order by amount of times accessed
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=False))
analyze(sites_count_sorted, prompt) # Analyzes the data given in dictionary
