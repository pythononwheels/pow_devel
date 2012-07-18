#
# POW Helpers for mako and html
# 

def css_include_tag(base, cssfile):
    return (os.path.normpath(os.path.join(base,cssfile)))

def test_helper():
    return "test_helper() worked"
    
def mail_to(email):
    mailto = "<a href=\"mailto:%s\">%s</a>" % (email,email)
    return mailto

def link_to(link, text, options_dict = None):
    linkto_first = "<a href=\"%s\" " % (link)
    linkto_last = ">%s</a>" % (text)
    # Add html-options if there are any
    if options_dict != None:
        for key in options_dict:
            linkto_first += "%s=\"%s\"" % (key, options_dict[key])
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