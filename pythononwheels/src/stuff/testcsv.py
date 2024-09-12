import csv
import json
import sys

#
# This is a sample file to demonstrat how to
# create PoW Models from csv


inf = open("sample.csv", "r")
#
# read the csv and convert to json on the fly
#
for row in csv.DictReader(inf):
    print(row)
    json.dump(row, sys.stdout)
    sys.stdout.write('\n')
    # Now setup your  models.
    #m = MyModel()
    #m.init_from_json(data=json.dump(row, sys.stdout))

print("...................")
#
# read the csv and get a list of strings 
# first row contains the keys
#
inf.close()
inf = open("sample.csv", "r")

for idx, row in enumerate(csv.reader(inf)):
    print( str(idx) +  " :" + str(row))
    if idx == 0:
        keys = row
    # Now setup your  models.
    #m = MyModel()
    #m.init_from_csv(keys=keys, data=row)