#!/usr/bin/env python

import json
import shutil
import urllib2
from datetime import datetime

"""Quick and dirty script for generating an index of Khan Academy content. 
Looks at topic titles, exercise titles, and video titles and keywords to 
produce a simple hash that can be used to test whether or not a given keyword 
is related to any videos or exercises. The source data is from the topic tree 
public API method."""

API_ENDPOINT = "http://khanacademy.org/api/v1/topictree"
BASE_VERSION = "1.0"
      
def parse(tree, stopwords, data={}):
  children = tree.get("children")
  if children: 
    for child in children: 
      data = parse(child, stopwords, data)
  kind = tree.get("kind")
  if kind == "Topic": 
    keywords = tree["title"].split()
  if kind == "Video": 
    keywords = tree["title"].split() + tree["keywords"].split(", ")
  elif kind == "Exercise": 
    keywords = tree["display_name"].split()
  keywords = filter(lambda k: k not in stopwords, keywords)
  for keyword in keywords: 
    data[keyword] = 1
  return data
      
def main(): 
  print "Retrieving topic tree"
  try: 
    topic_tree = json.loads(urllib2.urlopen(API_ENDPOINT).read())
  except: 
    print "Topic tree retrieval failed. Something is wrong with the API."
    return
    
  print "Generating index"
  with open("stopwords.json") as f: 
    stopwords = json.loads(f.read())
  stopwords = stopwords + [str(i) for i in range(10)] + [""]
  data = parse(topic_tree, stopwords)
  with open("extension/khantent.json", 'w') as f: 
    f.write(json.dumps(data))
  print "Index of %s items created" % len(data)
  
  print "Updating manifest.json"
  with open("manifest.template.json") as f: 
    manifest = json.loads(f.read())
  # http://code.google.com/chrome/extensions/manifest.html#version
  version_format = "%-y%-m.%-d%-H.%-M%-S"
  manifest["version"] = datetime.strftime(datetime.today(), version_format)
  with open("extension/manifest.json", 'w') as f: 
    f.write(json.dumps(manifest))

  print "Creating archive for Chrome Web Store"
  shutil.make_archive("khanpedia", "zip", "extension")
  
if __name__ == '__main__':
  main()
