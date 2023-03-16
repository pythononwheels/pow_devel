#
# dev config
#

from .config import *

# just overwrite the config options you want to change from the 
# standard config.py as in the example below.

server_settings["port"] = 9090
myapp["logfile"] = "sometest.log"