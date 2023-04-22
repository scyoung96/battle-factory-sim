from glob import glob
import os
import re
from tqdm import tqdm as prog

path = "sprites/"
files = glob(path + "*")
done = []

try:
    os.remove(path + ".TODO.txt")
except:
    pass

for i in prog(files):
    # get rid of anything that isn't a png or a home icon
    if re.search("0 XY.png", i) or re.search("Egg ", i) or not re.search("png", i) or not re.search("HOME", i):
        if re.search("0 XY.png", i):
            continue
        if os.path.isdir(i):
            for j in glob(i + "/*"):
                os.remove(j)
            os.rmdir(i)
        else:
            os.remove(i)
    else:
        num = re.search(r"(\d+)", i).group(1)
        try:
            code = re.search(r"\d+([a-zA-Z]+) ", i).group(1)
        except AttributeError:
            code = ""
        if num + code not in done:
            number = num.zfill(4)

# NOTE: special cases 
            if num == "479": # Rotom
                try:
                    form = re.search(r"F(\d)", i).group(1)
                    code = f"F{form}"
                except AttributeError:
                    form = ""
                    code = ""
            elif num == "718": # Zygarde
                form = re.search(r"-(\d+)", i).group(1)
                code = f"F{form}"
            elif num in ["421","422","423","550","555","592","593","648","658","669","670","671","681","716","774","801","875","877","893","931","964","999", "1007", "1008"]: # Cherrim, Shellos, Gastrodon, Basculin, Darmanitan, Frillish, Jellicent, Meloetta, Greninja, Flabebe, Floette, Florges, Aegislash, Xerneas, Wishiwashi, Minior, Magearna, Eiscue, Morpeko, Zarude, Squakabilly, Palafin, Gimmeghoul, Koraidon, Miraidon
                if code in ["E","F","P","Z","GZ","BB","EF","A","S","G","I","V","Y","O","R","H","B","W","Y","D","NF"]:
                    if num in ["555", "931"] and code in ["G", "Y"]:
                        pass
                    else:
                        os.remove(i)
                        continue
# NOTE: end special cases

            os.rename(i, path + f"{number}{code}.png")
            done.append(num + code)
        else:
            os.remove(i)
