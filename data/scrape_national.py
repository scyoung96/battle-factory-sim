import re
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm as prog

nat_ref = {}

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
r = requests.get(url)
soup = bs(r.content, "html.parser")

trs = soup.select("tr[style='background:#FFF']")
for row in prog(trs):
    try:
        num = row.select('td[style="font-family:monospace,monospace"]')[0].text[1:].strip().zfill(4)
    except IndexError:
        continue
    name = row.select('td:nth-child(3) a')[0].text.strip()

    nat_ref[num] = name

with open("data/natdex_reference.py", "w") as f:
    f.write("natdex_ref = " + str(nat_ref))
