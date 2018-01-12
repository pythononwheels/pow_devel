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
import {{appname}}.powlib as lib
import {{appname}}.config as cfg
import shutil

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_scaffold(handler_name, appname=None, view_type=None):
    """ 
        generates the plain html view scaffolding
    """
    
    loader = template.Loader(cfg.templates["stubs_path"])
    handler_class_name = camel_case(handler_name)
    #
    # generate the scaffolding
    #
    #rest_methods = ["show", "list", "page",  "new", "create", "edit", "update", "destroy"]

    views = ["show", "list", "page", "edit","new"]
    print(40*"-")
    print(" generating Scaffolds for: " + handler_name)
    print(" view_type: " +view_type)
    print(40*"-")
    for view in views:
        template_file =  os.path.join(cfg.templates["stubs_path"], "scaffold_" + view + "_view." + view_type )
        #
        # copy to dest dir first
        #
        opath = os.path.join(cfg.templates["views_path"], str.lower(handler_class_name))
        if not os.path.exists(opath):
            os.makedirs(opath)
        
        ofile_name = os.path.join( opath, str.lower(handler_class_name) + "_" + view + ".tmpl")
        shutil.copy( template_file, ofile_name )
        #
        # then process the template
        #
        # ofile = open(ofile_name, "wb")
        # res = loader.load(template_file).generate( 
        #     handler_name=handler_name, 
        #     handler_class_name=handler_class_name,
        #     appname=appname
        #     )
        # ofile.write(res)
        # ofile.close()
        print("... created view: " + ofile_name)
        print("...    -> using template: " + os.path.basename(template_file))
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="handler_name", help='-n handler_name',
                        required=True)
    
    parser.add_argument('-t', "--type", action="store", 
                        dest="view_type", help='-t bs4 (for bootstrap 4) || -t sui (for semantic ui)',
                        required=True, default="bs4")
    
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    print("CamelCased handler name: ", camel_case(args.handler_name))
    generate_scaffold(args.handler_name, appname="{{appname}}", view_type=args.view_type)

if __name__ == "__main__":
    main()

