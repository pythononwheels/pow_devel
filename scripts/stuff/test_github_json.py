#
#
# test github api access
#
#

import json
import requests
import sys

if __name__ == "__main__":
    user = raw_input("github user to check:")
    pwd = raw_input("github password for %s:" % (user) )
    repo = raw_input("github repo to check:")
      
    r = requests.get('https://api.github.com/repos/%s/%s/beta1_auth_and_relate/commits' % (user, repo), auth=(user, pwd))
    #print json.dumps(r.json, sort_keys=True, indent=4)
    ostr = ""
    for di in r.json:
        #ostr += "date: " + di["commit"]["author"]["date"] + "\n"
        #ostr += "author name: "+ di["commit"]["author"]["name"] +  "\n"
        #ostr += "author email: " + di["commit"]["author"]["email"] + "\n"
        #ostr += "commit message: " + di["commit"]["message"] + "\n"
        #ostr += "commit url: " + di["commit"]["url"] + "\n"
        print di
    of = open("out.txt", "w")
    of.write(ostr)
    of.close()   
    sys.exit()