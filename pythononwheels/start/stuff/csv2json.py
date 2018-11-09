
#
# Convert a csv to a multiline json
# utility to convert also with the goal to use the
# json2cerberus utility afterwatrs to create a schema from a csv
# (csv->json->schema)
# 
# khz 2018
#

import csv
import simplejson as json
import click

@click.command()
@click.option('--infile', help='csv input filename')
@click.option('--delimiter', default=",", help='csv delimiter')
def csv_to_json(infile, delimiter):
    csvfile = open(infile, 'r')
    jsonfile = open(infile + '.json', 'w')

    reader = csv.reader(csvfile)
    i = next(reader)
    columns=i
    print(columns)
    reader = csv.DictReader( csvfile, columns)
    olist=[]
    for row in reader:
        #print(row)
        olist.append(dict(row))
        #json.dump(row, jsonfile)
        #jsonfile.write('\n')
    json.dump(olist, jsonfile)

if __name__ == "__main__":
    csv_to_json()


