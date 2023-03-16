#
#
# pow server
# khz / 2016
#

import tornado.httpserver
import os
import os.path
import sys
import {{appname}}.conf.config as cfg
from {{appname}}.lib.powlib import merge_two_dicts
from {{appname}}.lib.application import Application, log_handler
import logging
import asyncio
import sys
import ssl

# asyncio issue 
# see: https://github.com/tornadoweb/tornado/issues/2751
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

powstr=r"""
  _____       _   _                  ____    __          ___               _     
 |  __ \     | | | |                / __ \   \ \        / / |             | |    
 | |__) |   _| |_| |__   ___  _ __ | |  | |_ _\ \  /\  / /| |__   ___  ___| |___ 
 |  ___/ | | | __| '_ \ / _ \| '_ \| |  | | '_ \ \/  \/ / | '_ \ / _ \/ _ \ / __|
 | |   | |_| | |_| | | | (_) | | | | |__| | | | \  /\  /  | | | |  __/  __/ \__ \\ 
 |_|    \__, |\__|_| |_|\___/|_| |_|\____/|_| |_|\/  \/   |_| |_|\___|\___|_|___/
         __/ |                                                                   
        |___/                                                                    
"""

def main(stdout=False):    
    print(powstr)
    print(60*"-")
    print("Collecting the routes")
    print(60*"-")
    app=Application()
    if stdout:
        print() 
    #tornado.options.parse_command_line()
    #from tornado.log import enable_pretty_logging
    #enable_pretty_logging()
    #print(dir(tornado.options.options))

    tornado.options.options.log_file_prefix = cfg.myapp["logfile"]
    tornado.options.options.log_file_num_backups=5
    # size of a single logfile
    tornado.options.options.log_file_max_size = 10 * 1000 * 1000
    
    tornado.options.parse_command_line()

    gen_logger = logging.getLogger("tornado.general")
    gen_logger.addHandler(log_handler)

    access_logger = logging.getLogger("tornado.access")
    access_logger.addHandler(log_handler)
    #print(access_logger.handlers)
    #for elem in access_logger.handlers:
    #    print(dir(elem))


    app_logger = logging.getLogger("tornado.application")
    app_logger.addHandler(log_handler)

    #app = tornado.web.Application(handlers=routes, **cfg.app_settings)
    #if stdout:
    #    print(60*"-")
    #    print("Databases: " )
    #    print(60*"-")
    #    #for idx, elem in enumerate(cfg.database["sql"]):
    #    print("  SQL-DB     : enabled: {} type: {}".format(
    #            str(cfg.database["sql"]["enabled"]), cfg.database["sql"]["type"] ))
    #    print("  TinyDB     : enabled: {}".format( str(cfg.database["tinydb"]["enabled"])))
    #    print("  MongoDB    : enabled: {}".format( str(cfg.database["mongodb"]["enabled"])))
    #    for idx, elem in enumerate(cfg.database["mongodb"]["indexes"]):
    #        print("      Index #{:2}: collection: {:12} def: {} ".format(
    #            str(idx), elem, cfg.database["mongodb"]["indexes"][elem] ))
    #    print("  Elastic    : enabled: {}".format( str(cfg.database["elastic"]["enabled"])))
    #app=Application()
    #print(app)
    if stdout:
        #print(app.handlers)
        print()
        print(60*"-")
        print("Final routes (order matters from here on ;) " )
        print(60*"-")
        
        for idx,elem in enumerate(app.handlers):
            print("ROUTE {:2}: pattern: {:50}  handler: {:20} ".format( 
               str(idx), str(elem[0])[0:48], str(elem[1].__name__) ))
                        
    
    

    if cfg.app_settings["ssl"]:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cfg.app_settings["ssl_options"]["certfile"], cfg.app_settings["ssl_options"]["keyfile"])
        cfg.app_settings["protocol"] = "https"
        http_server = tornado.httpserver.HTTPServer(app,ssl_options = ssl_ctx)
    else:
        cfg.app_settings["protocol"] = "http"
        http_server = tornado.httpserver.HTTPServer(app)

    print()
    print(60*"-")
    print("starting the PythonOnWheels server ")
    print(60*"-")
    print(f"visit: {cfg.app_settings['protocol']}://{cfg.app_settings['host']}:{cfg.app_settings['port']}")
    print("starting...")

    
    http_server.listen(cfg.app_settings["port"])
    ioloop = tornado.ioloop.IOLoop.instance()
    if cfg.app_settings["IOLoop.set_blocking_log_threshold"]:
        ioloop.set_blocking_log_threshold( cfg.app_settings["IOLoop.set_blocking_log_threshold"])
    ioloop.start()
    #tornado.ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main(stdout=True)

