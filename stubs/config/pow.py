#
# project_name = python on wheels
# author = khz
# author_email = khz@pythononwheels.org
# short_description = python rapid web app generator framework
# homepage_base_url = http://www.pythononwheels.org
#
# New style main config file for PythonOnWheels.
# Uses python data structures (dict, list etc) instead of ini-style
# way better handling ;)
# Date: July 2012
# 

global_conf = { 
    "ENV"   :   "development",
    "DEFAULT_TEMPLATE"  :   "hero.tmpl",
    "DEFAULT_ENCODING"  :   "utf-8",
    "PORT"  :   "8080"
}

routes = {
     "default"  :   "/app/welcome" 
}