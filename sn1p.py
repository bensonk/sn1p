#!/usr/bin/env python
import sys, os.path, json
from urllib import urlopen, urlencode

key_file = file(os.path.join(os.path.expanduser('~'), ".sn1p.key"))
API_KEY = key_file.readline()
key_file.close()
API_URL = "http://sn1p.me"
debug = False

def get(path):
  url = API_URL + path + "?key=" + API_KEY
  if debug: print(url)
  remote = urlopen(url)
  data = json.loads(remote.read())
  remote.close()
  return data

def post(path, data):
  url = API_URL + path
  if debug: print(url)
  data['key'] = API_KEY
  postdata = urlencode(data)
  remote = urlopen(url, postdata)
  raw_data = remote.read()
  try:
    data = json.loads()
  except:
    data = None
  remote.close()
  return data

def print_snip_list():
  snips = [ s['snippet'] for s in get("/snippets.json") ]
  for snip in snips:
    print("{name}".format(**snip))

def print_snip(id):
  snip = get("/snippets/{0}.json".format(id))
  print(snip['snippet']['body'])

def new_snip(name):
  body = "".join(sys.stdin.readlines())
  data = { 'snippet[name]': name, 'snippet[body]': body }
  post("/snippets.json", data)

def remove_snip(id):
  post("/snippets/destroy/{0}.json".format(id), { "method": "delete" })

def usage():
  print """Usage: ./sn1p.py help # This message
  ./sn1p.py <id or name> # gets a snippet
  ./sn1p.py get <id or name> # also gets a snippet
  ./sn1p.py remove <id or name> # Deletes a snippet
  ./sn1p.py help # This help message"""

commands = {
      "list": print_snip_list,
      "get": print_snip,
      "new": new_snip,
      "remove": remove_snip,
      "help": usage
    }

def dispatch(args):
  if args: cmd = args.pop(0)
  else: cmd = "list"

  if cmd in commands:
    commands[cmd](*args)
  else:
    print_snip(cmd)

if __name__ == "__main__":
  dispatch(sys.argv[1:])
