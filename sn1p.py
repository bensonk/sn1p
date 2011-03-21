#!/usr/bin/env python
import sys, os.path, json
from urllib import urlopen
key_file = file(os.path.join(os.path.expanduser('~'), ".sn1p.key"))
API_KEY = key_file.readline()
key_file.close()
API_URL = "http://sn1p.me"

def get(path):
  url = API_URL + path + "?key=" + API_KEY
  remote = urlopen(url)
  data = json.loads(remote.read())
  remote.close()
  return data

def get_snip_list():
  return [ s['snippet'] for s in get("/snippets.json") ]

def print_snip_list():
  for snip in get_snip_list():
    print snip['name']


if __name__ == "__main__":
  print_snip_list()
