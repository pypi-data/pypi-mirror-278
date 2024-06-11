from tabulate import tabulate
from termcolor import colored
import re
import requests

def get_domain(url):
  subdomains = []

  req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=url))

  for index, value in enumerate(req.json()):
      subdomains.extend(value["name_value"].split("\n"))

  subdomains = list(sorted(set(subdomains)))

  header = "Subdomain" if len(subdomains) == 1 else "Subdomains"
  colored_header = colored(header, "red")
  data = [{colored_header: subdomain} for subdomain in subdomains]

  print(tabulate(data, headers="keys", tablefmt="grid"))
  print()
