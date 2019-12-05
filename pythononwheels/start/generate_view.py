import click
import tornado.template as template
import os.path
#import timeit
import {{appname}}.conf.config as cfg
import shutil 

@click.command()
@click.option('--name', help='set the view name')
#@click.option('--base', default="base.bs4", help='set the base view ')
#@click.option('--type', default="simple", help='simple skeleton or full template')
@click.option('--dir', default=".", help='set the output directory (join(views_path,dir) )')
#@click.option('--convstr', default=False, is_flag=True, help='try to convert strings to numbers first')
#@click.option('--skipcol', multiple=True, help='skip a column by column name')


def generate_view(name, dir):
    """ 
        generates plain tmpl views
        simple (skeleton only)
        or full fledgded bootstrap or semantic
    """
    loader = template.Loader(cfg.templates["stubs_path"])
    #
    # generate the view
    #
    print(40*"-")
    print(" generating view: " + name)
    #print(" view_type: " + type)
    print(40*"-")

    template_file =  os.path.join(cfg.templates["stubs_path"], "view_template.tmpl" )
    #
    # copy to dest dir first
    #
    opath = os.path.normpath(os.path.join(cfg.templates["views_path"], str.lower(dir)))
    # create the path if it does not exist
    if not os.path.exists(opath):
        os.makedirs(opath)
    
    ofile_name = os.path.join( opath, name + ".tmpl")
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

if __name__ == "__main__":
    generate_view()