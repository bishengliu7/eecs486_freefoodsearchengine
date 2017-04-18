from bs4 import BeautifulSoup
from urlparse import urlparse
import sys
from urlparse import urljoin
import requests
import csv

if __name__ == "__main__":
  # We only crawle URL that starts with base URL
  baseUrl = "http://events.umich.edu/event/"

  # We open a csvfile to store crawled events
  csvfile = open('final_events.csv', 'wb')
  eventwriter = csv.writer(csvfile, delimiter=',')
  eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags'])

  for eventId in range(1,41000):
    url = baseUrl + str(eventId)
    try:
      r = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
      print "Timeout"
      continue
    except:
      print "Connect error"
      continue

    soup = BeautifulSoup(r.text, "html.parser")

    # discard event with no title
    if len(soup.findAll("h2", { "class" : "page-title" })) > 0:
      continue

    event = {'id': eventId,
             'title': "",
             'desc': "",
             'loc': "",
             'date': [],
             'tags': []}

    # fetch event title
    if soup.findAll("h1", { "class" : "title" }):
      event['title'] = str(soup.findAll("h1", { "class" : "title" })[0].get_text().encode('utf-8'))
    else:
      continue
    
    # fetch event description
    fetch = soup.findAll("div", { "class" : "event-description" })
    if fetch:
      event['desc'] = str(' '.join(fetch[0].get_text().encode('utf-8').split()))
      if not event['desc']:
         continue
    else:
      continue

    # fetch event location
    fetch = soup.findAll("i", { "class" : "fa-location-arrow" })
    if fetch:
      event['loc'] = str(' '.join(fetch[0].parent.get_text().encode('utf-8').split()))
    
    # fetch event time
    for i in soup.findAll("time"):
      event['date'].append(str(i['datetime']))

    # fetch event tages
    for i in soup.findAll("i", { "class" : "fa-tags" }):
      event["tags"].append(str(i.parent.get_text().encode('utf-8').strip()))

    # print(eventId)

    # write to csv file
    eventwriter.writerow([event['id'], event['title'], event['desc'], event['loc'],
       event['date'], event['tags']])
          
