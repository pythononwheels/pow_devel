#
# POW Helpers for mako and html
# 

def css_include_tag(base, cssfile):
    return (os.path.normpath(os.path.join(base,cssfile)))

def test_helper():
    return "test_helper() worked"

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
        pass
        
        
    input_last = ">"
    if options_dict != None:
        add_html_options(options_dict)
    input = inpout_first + inpuot_last
    return input
    
def mail_to(email):
    mailto_first = "<a href=\"mailto:%s\"" % (email)
    mailto_last = ">%s</a>" % (email)
    if options_dict != None:
        add_html_options(options_dict)
    mailto = mailto_first + mailto_last
    return mailto


def link_to(link, text, options_dict = None):
    linkto_first = "<a href=\"%s\" " % (link)
    linkto_last = ">%s</a>" % (text)
    # Add html-options if there are any
    if options_dict != None:
        add_html_options(options_dict)
    linkto = linkto_first + linkto_last
    return linkto


def add_html_options(options_dict=None):
    ostr = ""
    if options_dict != None:
        for key in options_dict:
            ostr += "%s=\"%s\"" % (key, options_dict[key])
    return ostr

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

    function test_button() {
        var data =document.getElementById('ajax_input').value;           
        xml_http_post("/app/ajax", data, test_handle)
    }

    function test_handle(req) {
        var elem = document.getElementById('test_result')
        elem.innerHTML =  req.responseText
    }

    </script> <!-- End AJAX Test -->
    """
    
    return script