import dash_core_components as dcc
import dash_html_components as html
# see: https://github.com/ned2/slapdash/tree/master/slapdash   
# and: https://community.plot.ly/t/dash-bootstrap-and-datagrid-components-contrib/4904/6

def Row(children=None, **kwargs):
    """A convenience component that makes a Bootstrap row"""
    return html.Div(children=children, className='row', **kwargs)



def Col(children=None, bp=None, size=None, **kwargs):
    """A convenience component that makes a Bootstrap column"""
    if size is None and bp is None:
        col_class = 'col'
    elif bp is None:
        col_class = 'col-{}'.format(str(size))
    else:        
        col_class = 'col-{}-{}'.format(str(size), str(bp))
    return html.Div(children=children, className=col_class, **kwargs)



def Link(children=None, href='', **kwargs):
    # TODO: CSS pointer-events have been set to none for the nested anchor tag
    # so that clicking the link doesn't cause a page redirect to the target
    # link. This however means we lose some useful link hover behaviour.
    # https://github.com/plotly/dash-core-components/issues/129
    return dcc.Link(
        href=href,
        className='link',
        children=html.A(children, href=href),
        **kwargs
    )





def Fa(name):
    """A convenience component for adding Font Awesome icons"""
    return html.I(className="fa fa-{name}")