#
##
#
# test github api access
#
#

import json
import requests
import sys


class User(object):
    
    def __init__(self, name = "", password = ""):
        self.name = name
        self.password = password
    
    
def github.get_milestone_info(user, repo, milestone):
    r = requests.get('https://api.github.com/repos/%s/%s/milestones/%s' % (user,repo, milestone), auth=(user, pwd))
    #print json.dumps(r.json, sort_keys=True, indent=4)
    return r.json
    
def get_commit_info( user, repo, branch):
    r = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % (user,repo, branch), auth=(user, pwd))
    return r.json
    
if __name__ == "__main__":
    #user = raw_input("github user to check:")
    #pwd = raw_input("github password for %s:" % (user) )
    #repo = raw_input("github repo to check:")
    #branch = raw_input("branch for %s repo to check:" % (repo))
    user = User()
    user.name = "pythononwheels"
    user.password = "h0dde!1"
    repo = "pow_devel" 
    branch = "beta1_auth_and_relate"
    
    
    
    #ostr = ""
    #for di in r.json:
    #    ostr += "date: " + di["commit"]["author"]["date"] + "\n"
    #    ostr += "author name: "+ di["commit"]["author"]["name"] +  "\n"
    #    ostr += "author email: " + di["commit"]["author"]["email"] + "\n"
    #    ostr += "commit message: " + di["commit"]["message"] + "\n"
    #    ostr += "commit url: " + di["commit"]["url"] + "\n"
    #    print di
    #of = open("out.txt", "w")
    #of.write(ostr)
    #of.close()   
    sys.exit()
# test github api access
#
#

import json
import requests
import sys

if __name__ == "__main__":
    #user = raw_input("github user to check:")
    #pwd = raw_input("github password for %s:" % (user) )
    #repo = raw_input("github repo to check:")
    #branch = raw_input("branch for %s repo to check:" % (repo))
     
    user = "pythononwheels"
    pwd = "h0dde!1"
    repo = "pow_devel" 
    branch = "beta1_auth_and_relate"
    #r = requests.get('https://api.github.com/user/repos' , auth=(user, pwd))
    #print json.dumps(r.json, sort_keys=True, indent=4)
    
    r = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % (user,repo, branch), auth=(user, pwd))
    print json.dumps(r.json, sort_keys=True, indent=4)
    #ostr = ""
    #for di in r.json:
    #    ostr += "date: " + di["commit"]["author"]["date"] + "\n"
    #    ostr += "author name: "+ di["commit"]["author"]["name"] +  "\n"
    #    ostr += "author email: " + di["commit"]["author"]["email"] + "\n"
    #    ostr += "commit message: " + di["commit"]["message"] + "\n"
    #    ostr += "commit url: " + di["commit"]["url"] + "\n"
    #    print di
    #of = open("out.txt", "w")
    #of.write(ostr)
    #of.close()   
    sys.exit()