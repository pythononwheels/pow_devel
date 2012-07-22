#
# POW Helpers for mako and html
# 
import powlib

def css_include_tag(base, cssfile):
    return (os.path.normpath(os.path.join(base,cssfile)))

def test_helper():
    return "test_helper() worked"

def generate_hidden(model, hidden_list=None):
    ostr = ""
    if hidden_list == None:
        hidden_list = powlib.hidden_list
    for colname in model.getColumns():
        if colname in hidden_list:
            ostr += '<input type="hidden" name="%s" value="%s"/>' % (colname, model.get(colname))
    
    return ostr
    
def form_input(name, value, options_dict=None, model=None, type=None):
    if model == None:
        # No model given, so always generate a standard text type or the given type input html field
        if type == None:
            input_first = "<input type='text' name='%s' value='%s'" % (name, value)
        else:
            input_first = "<input type='%s' name='%s' value='%s'" % (type, name, value)
    else:
        # model given, so create the right input-type according to the models datatype
        # the field is the same as the given name. So type of model.name determines the input-type
        mod = pow_lib.load_class(string.capitalize(model), model)
        input_first = "<"
        statement = "mod.%s" % (name)
        curr_type = eval(statement)
        if curr_type == sqlalchemy.types.INTEGER:
            pass
        elif curr_type == sqlalchemy.types.TEXT:
            pass
        elif curr_type == sqlalchemy.types.VARCHAR:
            pass
        
    input_last = ">"
    if options_dict != None:
        add_html_options(options_dict)
    input = inpout_first + inpuot_last
    return input
    
def create_link(model, text=None):
    if text == None:
        retstr = '<i class="icon-plus"></i>&nbsp;<a href="./create">create</a>' 
    else:
        retstr = '<i class="icon-plus"></i>&nbsp;<a href="./create">%s</a>' % (text)
    return retstr
    
def delete_link( model, text=None ):
    if text == None:
        retstr = '<i class="icon-remove"></i>&nbsp;<a href="./delete?id=%s">delete</a>' % (model)
    else:
        retstr = '<i class="icon-remove"></i>&nbsp;<a href="./delete?id=%s">%s</a>' % (model,text)
    return retstr

def show_link( model, text=None):
    if text == None:
        retstr ='<i class="icon-eye-open"></i>&nbsp;<a href="./show?id=%s">show</a>' % (model)
    else:
        retstr = '<i class="icon-eye-open"></i>&nbsp;<a href="./show?id=%s">%s</a>' % (model,text)
    return retstr
    
def edit_link(model_id, text=None):
    if text == None:
        retstr = '<i class="icon-edit"></i>&nbsp;<a href="./edit?id=%s">edit</a>' % (model_id)
    else:
        retstr = '<i class="icon-edit"></i>&nbsp;<a href="./edit?id=%s">%s</a>' % (model_id,text)
    return retstr
        
def flash_message():
    msg = """
    %if powdict["FLASHTEXT"] != "":
    	<div class="alert alert-${powdict["FLASHTYPE"]}">
    		<button class="close" data-dismiss="alert">x</button>
    		${powdict["FLASHTEXT"]}
    	</div
    %endif
    """
    return msg

def add_html_options(options_dict=None):
    ostr = ""
    if options_dict != None:
        for key in options_dict:
            # handle options_dict as dict (had problems with Mako before 0.72 ??)
            ostr += '%s="%s"' % (key, options_dict[key])
            # handle options_dict as list of tupels. So enable this with Mako before 0.72
            #ostr += "%s=\"%s\"" % (key[0],key[1])
    return ostr  

def mail_to(email):
    mailto_first = "<a href=\"mailto:%s\"" % (email)
    mailto_last = ">%s</a>" % (email)
    mailto_first += add_html_options(options_dict)
    mailto = mailto_first + mailto_last
    return mailto


def link_to(link, text, options_dict=None):
    linkto_first = "<a href=\"%s\"" % (link)
    linkto_last = ">%s</a>" % (text)
    linkto = ""
    # Add html-options if there are any
    linkto_first += add_html_options(options_dict)
    linkto = linkto_first + linkto_last
    return linkto

def enable_ajax():
    return enable_xml_http_post()
    
def enable_xml_http_post():
    script = """
    <!-- Start AJAX Test, see: http://stackoverflow.com/questions/336866/how-to-implement-a-minimal-server-for-ajax-in-python -->
     <script type="text/javascript">

    function xml_http_post(url, data, callback) {
        var req = false;
        try {
            // Firefox, Opera 8.0+, Safari
            req = new XMLHttpRequest();
        }
        catch (e) {
            // Internet Explorer
            try {
                req = new ActiveXObject("Msxml2.XMLHTTP");
            }
            catch (e) {
                try {
                    req = new ActiveXObject("Microsoft.XMLHTTP");
                }
                catch (e) {
                    alert("Your browser does not support AJAX!");
                    return false;
                }
            }
        }
        
        req.open("POST", url, true);
        req.onreadystatechange = function() {
            if (req.readyState == 4) {
                callback(req);
            }
        }
        req.send(data);
    }

    function send_request() {
        var data=document.getElementById('ajax_input').value;           
        xml_http_post("/app/ajax", data, handle_response)
    }

    function handle_response(req) {
        var elem = document.getElementById('test_result')
        elem.innerHTML =  req.responseText
    }

    </script> <!-- End AJAX Test -->
    """
    
    return script