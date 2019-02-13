.. figure:: http://www.pythononwheels.org/static/images/pow_logo_300.png
   :alt: Pow logo

   Pow logo

The quick and easy generative Webframework for python3. Ready to go!
====================================================================

    Based on the ruby on rails principles. Generators for
    models/controllers/views/migrations..., convention over
    configuration, and PoW gets out of the way if you want it.

Hello World
===========

::

    @app.make_routes()
    class HelloHandler(BaseHandler):
        @route(r'/hello', dispatch=["get"])
        def hello(self):
            self.write("Hello world!")

Installation:
-------------

``pip install -U pythononwheels``

Everything you need on board. Batteries included.
=================================================

`PythonOnWheels <https://www.pythononwheels.org/>`__ is a generative,
Rapid Application Development, non intrusive web framework for python.
You need no extra tools to start. Everything from DB to Webserver and
template engine is included. But you are not forced to use them and can
go raw or easily include the modules and tools of your choice tools
whenever you want.

Based on a very Strong foundation:
==================================

-  python 3.x
-  `tornado <http://www.tornadoweb.org/en/stable/>`__ webserver
-  Supported SQL Databases
-  SQL: `sqlalchemy <https://www.sqlalchemy.org/>`__ ORM (SQLite, MySQL,
   PostgreSQL, MS-SQL, Oracle, and more ..)
-  Database Migrations onboard (based on alembic) generated behind the
   scenes
-  NoSQL:
   `tinyDB <https://tinydb.readthedocs.io/en/latest/index.html>`__,
   `MongoDB <https://www.mongodb.com/>`__,
   `elasticsearch <https://www.elastic.co/products/elasticsearch>`__
-  `cerberus <http://docs.python-cerberus.org/en/stable/>`__ schemas and
   validation on board
-  tornado templates
-  css Frameworks: `bootstrap4 <https://getbootstrap.com/>`__ and
   `semanticUI <https://semantic-ui.com/>`__

Probably the most simple SQL relations out there!
=================================================

Based on sqlalchemy. With PythonOnWheels you simply add a class
decorator like

::

    @relation.has_many("comments")
    class Post(Base):
        # All your Post model code below here ..
        .....

to your SQL Post-model and every Post can have comments. It will be
automatically mapped to the DB (SQLite, Postgres, MySQL, MariaDb,
Oracle, MSSQL ...) and to all related comment Models. DB Migrations are
created automatically in the background.

supported relation types are:
-----------------------------

-  has\_many("comments")(decorated class has many comments.)
-  many\_to\_many("comments")(decorated class has many to many with
   comments)
-  belongs\_to("comments")(decorated class belongs to comments.)
-  one\_to\_one("comments")(decorated class has one to one with
   comments)
-  tree() (decorated class has adjacence list (is a tree)

All pow models (SQL or NoSQL) use a `cerberus <http://docs.python-cerberus.org/en/stable/>`__ schema as definition.
===================================================================================================================

This means you have validation on board for every model and you can easily switch from SQL to NoSQL
---------------------------------------------------------------------------------------------------

-  the @relation.setup\_schema() decorator will map this schema to a
   vaild sqlalchemy (or specific NoSQL) column definition set.
-  SQL only: model will also automatically get all the right
   Foreign\_Keys and python attributes to create a has\_many
   relationship to the comments model. This is all done for you with the
   @relation.has\_many("comments") @relation.has\_many("comments")
   @relation.setup\_schema()

::

    class Post(Base):
    #
    # Schema definition with the new (cerberus) schema style
    # which offer you immediate validation
    #
    schema = {
        # string sqltypes can be TEXT or UNICODE or nothing
        'author': {'type': 'string', 'maxlength' : 35 },
        'title' : {'type': 'string', "required" : True },
        'text'  : {'type': 'string' },
        'votes' : {'type': 'integer' },
        'status': {'type': 'string', "allowed" : ["backlog", "wip", "done"] },
    }

    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here

Probably the most simple RESTrouting out there! One decorator. Done!
====================================================================

With PythonOnWheels you simply add a class decorator like
---------------------------------------------------------

::

    @app.add_rest_routes("basename") 

to your handler and you get all the typical REST routes mapped to the
according CRUD methods of your handler class.

By the way: this is what generate\_handler generates for you when you use the --rest parameter:
-----------------------------------------------------------------------------------------------

::

    @app.add_rest_routes("rest_test")
    class RestTest(BaseHandler):
        # 
        # every pow handler automatically gets these RESTful routes
        # when you add the : app.add_rest_routes() decorator.
        #
        # 1  GET    /resttest                           #=> list
        # 2  GET    /resttest/<uuid:identifier>         #=> show
        # 3  GET    /resttest/new                       #=> new
        # 4  GET    /resttest/<uuid:identifier>/edit    #=> edit 
        # 5  GET    /resttest/page/<uuid:identifier>    #=> page
        # 6  GET    /resttest/search                    #=> search
        # 7  PUT    /resttest/<uuid:identifier>         #=> update
        # 8  PUT    /resttest                           #=> update (You have to send the id as json payload)
        # 9  POST   /resttest                           #=> create
        # 10 DELETE /resttest/<uuid:identifier>         #=> destroy
        # ...

Routing: RegEx and Flask like routes included .
===============================================

You can set routes by simply adding a class decorator to the handler
class or decorate methods directly. ~\ :sub:`~` @route("/",
dispatch=["get"]) ~\ :sub:`~`

PythonOnWheels will then call the index method of your handler if the
route and the HTTP method matches.

Example for Flask like routing:
-------------------------------

::

    @app.make_method_routes()
    class HelloHandler(BaseHandler):
        @route(r'/hello/<int:identifier>', dispatch=["get"])
        def hello(self, identifier=None):
            self.write("Hello world! " + str(identifier))

For Regex routes:
-----------------

::

    @app.add_route("/test/([0-9]+)*", dispatch={"get" : "test"})

to add a direct route: matching the regular expression : /test/([0-9+])
and then calling the given method of your handler class. The regex group
([0-9+]) will be handed as the first parameter to test(self, index)

Model Validation on board with cerberus schemas.
================================================

All Model Schemas are Cerberus schemas automatically. So thats easy.
~\ :sub:`~` model.validate() => executes cerberus validator ~\ :sub:`~`

And finally: a super easy workflow. Quick to start, all the basics on
board and easy to expand: generative approach (but not noisy)

-  generate\_app script
-  generate\_models script (You probably want to store some data)
-  Optionally generate\_migrations script (only needed for SQL DBs)
-  generate\_handlers (aka controllers to define your logic and API)
-  start the server (python server.py) done

The vision:
===========

    If you want start to develop your web-application and focus on the
    App, instead of the frameworks, you are in the right place.
    PythonOnWheels feels right if you do not recognize that you use it.

Enjoy!
======

See `getting
started <http://www.pythononwheels.org/article/7de74cc6-8af2-45ac-b619-eea61e4da44f>`__
or go to the
`documentation <http://www.pythononwheels.org/article/2160fdfd-fc9f-4380-aeb3-bc13d2c201e0>`__


For more check: `The PythonOnWheels Homepage <http://www.pythononwheels.org>`__
-------------------------------------------------------------------------------
