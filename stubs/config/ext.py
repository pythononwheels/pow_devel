#
# configuration file for PythonOnWheels extensions
# all extensions shall by convention be placed in
# appname/ext dir. Any specific subdir might be chosen 
# but needs to be configured here.
# You can take the pow_auth and validation extensions as example.
#
#

# list of available extensions.
# Format: ( "ext_name", enabled? ), where enabled can be True or False
extensions = [ 
    ("auth", True)
    ("validate", False)
]

# extension specific dictionary for extension configuration.
# dir is the directory inside appname/ext where pow will look for the module.
# module specifies the main extension module to load.
auth = {
    "dir" : "auth",
    "module" : "pow_auth"
}

validate = {
    "dir" : "validate",
    "module" : "pow_validate"
}