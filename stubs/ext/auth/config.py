#
# configuration for the PoW authentication plugin
#
# cut this and add it to the ext.py file in the confid directory.
# TODO: do this automatically in the setup.py of each plugin
#  


auth = {
    "dir" : "auth",
    "module" : "auth",
    "models_dir" : "models",
    "controllers_dir" : "controllers",
    "views_dir" : "views"
}


# also enable the plugin in ext.py by adding:
#    ("auth", True)
# to the extensions list 