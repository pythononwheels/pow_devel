#
# werkzeug routing test
#

from werkzeug import routing

# pow routes look currently like this:
# @app.add_route("/thanks/([0-9]+)*", dispatch={"get": "testme"})
# testme the looks like:
# def testme(self, index=0 ): 
#   ...
# OR (REST example)
# r"/post/(?P<id>.+)/edit/?" , { "get" : "edit", "params" : ["id"] }),
# =>


# werkzeug routes have the following form
# Rule('/browse/<int:id>/', endpoint='kb/browse'),
