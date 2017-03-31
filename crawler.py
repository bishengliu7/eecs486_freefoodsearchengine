from bs4 import BeautifulSoup
from urlparse import urlparse
import requests
import sys
from collections import defaultdict
from urlparse import urljoin

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
  if len(sys.argv) < 3:
    print ("Missing arguments")
    exit(1)
  urlFile = str(sys.argv[1])
  maxUrl = int(sys.argv[2])

  urls = []
  with open(urlFile, 'r') as infile:
    urls = infile.read().split('\n')

  visited = []
  viewed = set()
  links = defaultdict(list)

  for url in urls:
    viewed.add(url)

  while len(visited) < maxUrl and len(urls) > 0:
    url = urls[0]
    del urls[0]

    try:
      r = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
      print "Timeout"
      print url
      continue
    except:
      print "Connect error"
      print (url)
      continue

    if "text/html" not in r.headers["content-type"]:
      continue

    visited.append(url)

    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all('a'):
      try:
        href = str(parseURL(link.get('href'), r.url))
      except UnicodeEncodeError:
        continue

      if href != "":
        if not (href in links[url]):
          links[url].append(href)
        if not (href in viewed):
          urls.append(href)
          viewed.add(href)

  with open('crawler.output', 'w') as outfile:
    for url in visited:
      outfile.write(url + '\n')

  with open('crawler.link', 'w') as outfile:
    for (k, l) in links.iteritems():
      for url in l:
        if url == "http://www.eecs.umich.edu":
          outfile.write(k + ' ' + visited[0] + '\n')
        elif url in visited:
          outfile.write(k + ' ' + url + '\n')
          