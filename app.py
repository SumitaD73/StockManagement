import glob
import json
import os
from pathlib import Path
from time import sleep
from datetime import datetime


def main(name):
    file_arr = glob.glob("./assets/{0}/*.jpg".format(name))
    
    print("Total: " + str(len(file_arr)) + " Files Found\n")
    
    img_path = r"./assets/{0}".format(name)

    id = 0

    new_arr = []

    for f in file_arr:
        now = datetime.now()
        dt_string = now.strftime("I%d%mD%Y%HC%M%SR")

        id += 1

        op = '{}/{}'.format(img_path, Path(f).name)
        np = '{}/{}'.format(img_path, dt_string + ".jpg")

        new_arr.append({
            "id": dt_string,
            "name": "---",
            "desc": "---",
            "size": "0",
            "imgs": "https://github.com/SumitaD73/StockManagement/blob/main/assets/{0}/{1}.jpg?raw=true".format(name, dt_string),
            "cost": "---",
            "stock": "true"
        })

        os.rename(op, np)

        print(np)

        sleep(1)

    file1 = open("./json/{0}.json".format(name), "w")
    file1.write(json.dumps(new_arr, sort_keys=False, indent=4))


if __name__ == '__main__':
    try:
        name_arr = ['saree', 'blouse', 'ornaments']

        for n in name_arr:
            main(n)
            print("")
            sleep(1)

        print("\n\nComplete.")
    except KeyboardInterrupt:
        print("\n\nCancelled.")
