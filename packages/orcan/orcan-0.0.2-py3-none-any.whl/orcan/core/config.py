import re

def clean_url(url):
  return re.sub(".*www\.", "", url, 1).split("/")[0].strip()

class Config:
  def __init__(self, args):
    if args.url is not None:
      self.url = clean_url(args.url)
    else:
      self.url = args.url
    self.domain = args.domain
    self.who = args.who
