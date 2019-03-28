
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
@click.option('--skipcol', multiple=True, help='skip a column by column name')
@click.option('--startrow', default=1, help='set the startrow number. [first=1]')
@click.option('--skiprow', multiple=True, help='skip row by rownumber')
@click.option('--delimiter', default=",", help='csv delimiter')
def csv_to_json(infile, convstr, delimiter, skipcol,startrow, skiprow):
    csvfile = open(infile, 'r')
    jsonfile = open(infile + '.json', 'w')

    reader = csv.reader(csvfile, delimiter=delimiter)
    i = next(reader)
    columns=i
    print(columns)
    #for col in skipcol:
    #    columns.remove(col)
    #print(columns)
    try:
        reader = csv.DictReader( csvfile, columns, delimiter=delimiter )
    except:
        raise
    olist=[]
    rowcount=1
    for row in reader:
        if rowcount > startrow:
            print(row)
            if convstr: 
                # try to convert str types to int,float
                for elem in row:
                    #print(" {} -> {} ".format(elem, row[elem]))
                    if isinstance(row[elem], str):
                        try:
                            row[elem] = int(row[elem])
                            #print("converted to int: {}".format(str(row[elem])))
                        except:
                            try:
                                row[elem] = float(row[elem])
                                #print("converted to float: {}".format(str(row[elem])))
                            except:
                                pass
            drow = dict(row)
            for col in skipcol:
                try:
                    del drow[col]
                except:
                    pass
            olist.append(drow)
        rowcount+=1
        #json.dump(row, jsonfile)
        #jsonfile.write('')
    json.dump(olist, jsonfile)

if __name__ == "__main__":
    csv_to_json()


