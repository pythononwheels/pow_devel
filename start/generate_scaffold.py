#
# generate scaffold
# generates the plain HTML view scaffolding for crud actions.
#
# index, show, list, edit, create, delete
#

import argparse
import tornado.template as template
import os.path
import timeit
import testapp.powlib as lib
import testapp.config as cfg


def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_scaffold(handler_name, appname={{appname}}):
    """ 
        generates the plain html view scaffolding
    """
    
    loader = template.Loader(cfg.templates["stubs_path"])
    handler_class_name = camel_case(handler_name)
    #
    # generate the scaffolding
    #
    #rest_methods = ["show", "list", "page",  "new", "create", "edit", "update", "destroy"]

    views = ["show", "list", "page"]

    for view in views:
        template_file =  "scaffold_" + view + "_view.tmpl"
        ofile_name = os.path.join(cfg.templates["view_path"], handler_name + "_" + view ".tmpl")
        ofile = open(ofile_name, "wb")
        res = loader.load(template_file).generate( 
            handler_name=handler_name, 
            handler_class_name=handler_class_name,
            appname=appname
            )
        ofile.write(res)
        ofile.close()
        print("... created view: " + ofile_name)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="handler_name", help='-n handler_name',
                        required=True)
    
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    print("CamelCased handler name: ", camel_case(args.name))
    generate_handler(args.name, args.db, appname="testapp")