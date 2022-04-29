import glob
import json
import os
from pathlib import Path
from time import sleep
from datetime import datetime
import mysql.connector
from PIL import Image

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="ideal_creations"
)


def trunctab(name):
    mycursor = mydb.cursor()
    sql = "TRUNCATE TABLE {0}".format(name)
    mycursor.execute(sql)
    mydb.commit()


def main(name):
    file_arr = glob.glob("./assets/{0}/*.jpg".format(name))
    
    print("Total: " + str(len(file_arr)) + " Files Found\n")
    
    img_path = r"./assets/{0}".format(name)

    id = 0

    new_arr = []

    for f in file_arr:
        image = Image.open(f)
        new_image = image.resize((1000, 1200))
        new_image.save(f)

        sleep(0.5)

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
            "stock": "true",
            "hidden": "false",
            "deleted": "false"
        })

        os.rename(op, np)

        sleep(0.5)

        mycursor = mydb.cursor()

        sql = "INSERT INTO {0} (id, name, description, size, image, price, stock, hidden, deleted) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)".format(name)
        val = ("", "Product Name", "Some Product Description", "0", dt_string, "---", "true", "false", "false")
        mycursor.execute(sql, val)

        mydb.commit()

        print("[" + str(id) + "] - " + str(new_image.size) + " - " + np)

        sleep(0.5)

    file1 = open("./json/{0}.json".format(name), "w")
    file1.write(json.dumps(new_arr, sort_keys=False, indent=4))


if __name__ == '__main__':
    try:
        name_arr = ['saree', 'blouse', 'ornaments']

        for n in name_arr:
            trunctab(n)
            sleep(0.5)
            print("")
            main(n)
            sleep(0.5)

        print("\n\nComplete.")
    except KeyboardInterrupt:
        print("\n\nCancelled.")
