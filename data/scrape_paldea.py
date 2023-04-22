import re
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm as prog

pal_nums = []
nat_nums = []

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Paldea_Pok%C3%A9dex_number"
r = requests.get(url)
soup = bs(r.content, "html.parser")

trs = soup.select("tr[style='background:#FFF']")
for row in prog(trs):
    tds = row.select('td[style="font-family:monospace,monospace"]')

    if len(tds) == 2:
        pal_num = tds[0].text[1:].strip().zfill(4)
        nat_num = tds[1].text[1:].strip().zfill(4)

        pal_nums.append(pal_num)
        nat_nums.append(nat_num)

    elif len(tds) == 1 and int(tds[0].text[1:].strip()) > int(nat_nums[-1]):
        pal_num = tds[0].text[1:].strip().zfill(4)

        pal_nums.append(pal_num)
        nat_nums.append(pal_num)

with open("data/pal_pokedex.py", "w") as f:
    f.write("pal_pokedex = " + str(nat_nums))
