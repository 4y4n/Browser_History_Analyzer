import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt


def parse(urls):
    try:
        parsed_url_components = urls.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print("URL format error!")


def analyze(results, input_prompt, plot_top=10):
    if input_prompt == "c":
        for site, visits in sites_count_sorted.items():
            print(site, visits)
    else:
        x = len(sites_count_sorted)
        for site, visits in dict(sites_count_sorted).items():
            x -= 1
            if x >= plot_top:
                del sites_count_sorted[site]
        plt.barh(list(results.keys()), list(results.values()))
        for site, visits in dict(sites_count_sorted).items():
            plt.text(visits, site, visits)
        plt.show()


dataPath = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
files = os.listdir(dataPath)
historyDB = os.path.join(dataPath, 'history')

c = sqlite3.connect(historyDB)
cursor = c.cursor()
selectStatement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(selectStatement)
result = cursor.fetchall()
times = []


sites_count = {}
for url, count in result:
    url = parse(url)
    if url in sites_count:
        sites_count[url] += 1
    else:
        sites_count[url] = 1

prompt = "yes"
while prompt != "c" and prompt != "p":
    prompt = str(input("[.] Type < c > to print or < p > to plot \n[>] "))
if prompt == "c":
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
else:
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=False))
analyze(sites_count_sorted, prompt)
