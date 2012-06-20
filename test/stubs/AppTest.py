#
# testscript for class App.App
#

import App
x = App.App()
sess = x.pao.getSession()

app = sess.query(App.App).filter_by(name='manuell').first()
#
# print the result
#
print app
print "name: " + app.name
print "path: " + app.path
print "currentversion: " + str(app.currentversion)
print "migrationversion: " + str(app.migrationversion)

#
# add a new user
#
a = App.App()
a.name = "test"
a.path = "test"
a.currentversion = 99
a.migrationversion = 99

sess.add(a)
sess.commit()





