from bs4 import BeautifulSoup
from urlparse import urlparse
import sys
from urlparse import urljoin
import requests
import csv

def parseURL(url, root):
  # empty url
  if not url or len(url) < 1:
    return ""

  # detect non-html
  suffix = [".jpg", ".pdf", ".png", ".mp3", ".mp4", ".zip", ".wmv", ".mov", ".ppt", ".eps"]
  if url[-4:].lower() in suffix:
    return ""

  if url[:4] != "http":
    url = urljoin(root, url)
  elif url[:5] == "https":
    url = "http" + url[5:]

  if url[-1] == '/':
    url = url[:-1]

  if url[:25] == "http://www.eecs.umich.edu":
    return url
  elif url[:21] == "http://eecs.umich.edu":
    return "http://www.eecs.umich.edu" + url[21:]
  else:
    return ""

if __name__ == "__main__":
  baseUrl = "http://events.umich.edu/event/"

  csvfile = open('events.csv', 'wb')
  eventwriter = csv.writer(csvfile, delimiter=',')
  eventwriter.writerow(['id', 'title', 'desc', 'loc', 'date', 'tags'])

  events = []
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

    if len(soup.findAll("h2", { "class" : "page-title" })) > 0:
      continue

    # print (eventId, soup.findAll("h1", { "class" : "title" }))
    # get title, description, location, date

    event = {'id': eventId,
             'title': "",
             'desc': "",
             'loc': "",
             'date': [],
             'tags': []}

    event['title'] = str(soup.findAll("h1", { "class" : "title" })[0].get_text().encode('utf-8'))

    fetch = soup.findAll("div", { "class" : "event-description" })
    if fetch:
      event['desc'] = str(' '.join(fetch[0].get_text().encode('utf-8').split()))
      if not event['desc']:
         continue
    else:
      continue

    fetch = soup.findAll("i", { "class" : "fa-location-arrow" })
    if fetch:
      event['loc'] = str(' '.join(fetch[0].parent.get_text().encode('utf-8').split()))
    
    for i in soup.findAll("time"):
      event['date'].append(str(i['datetime']))

    for i in soup.findAll("i", { "class" : "fa-tags" }):
      event["tags"].append(str(i.parent.get_text().encode('utf-8').strip()))

    print(eventId)

    # events.append(event)

    eventwriter.writerow([event['id'], event['title'], event['desc'], event['loc'], event['date']])
          