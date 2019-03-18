
#
# Convert a csv to a multiline json
# utility to convert also with the goal to use the
# json2cerberus utility afterwatrs to create a schema from a csv
# (csv->json->schema)
# 
# khz 2018
# update: 18.3.2019: added option to convert str types to int and float. See --convstr

import csv
import simplejson as json
import click

@click.command()
@click.option('--infile', help='csv input filename')
@click.option('--convstr', default=False, is_flag=True, help='try to convert strings to numbers first')
@click.option('--delimiter', default=",", help='csv delimiter')
def csv_to_json(infile, convstr, delimiter):
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
        if convstr: 
            # try to convert str types to int,float
            for elem in row:
                #print(" {} -> {} ".format(elem, row[elem]))
                if isinstance(row[elem], str):
                    try:
                        row[elem] = int(row[elem])
                        print("converted to int: {}".format(str(row[elem])))
                    except:
                        try:
                            row[elem] = float(row[elem])
                            print("converted to float: {}".format(str(row[elem])))
                        except:
                            pass
        olist.append(dict(row))
        #json.dump(row, jsonfile)
        #jsonfile.write('')
    json.dump(olist, jsonfile)

if __name__ == "__main__":
    csv_to_json()


