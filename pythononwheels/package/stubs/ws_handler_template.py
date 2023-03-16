
from {{appname}}.handlers.powwshandler import PowWsHandler
import simplejson as json
import datetime
from {{appname}}.conf.config import myapp, database
from {{appname}}.lib.application import app, route


@app.add_route(r"/websocket", dispatch={"ws" : None})
@app.make_routes()
class {{handler_class_name}}(PowWsHandler):
    """ 
        This is an example WebSocket Handler.
        You must adapt the protocol to your needs.

        This basic implementation exchanges 
        json messages of the format:

        {
            "method"    :   "<method_name>",
            "type"      :   "<message_type>",
            "data"      :   <json_data>
        }

        where:
         * method is the message to be called in the handler with the json as input paramter
         * type is: data or error
         * data is the payload. The <method> has to decide what to do with <data> probably taking <type> into concern.
        
        In this demo implementation the only implemented methood is 
        the <echo> method, which simply returns the data send to it.
        See def echo()
        
        Just copy, paste and rename it and add any functionality you need.
        Storing data in a Database, sending text and notofications to all other clients (chatroom)...
    """
    def __init__(self, *args, **kwargs):
        """ init    """
        super().__init__(*args, **kwargs)
        self.clients={}

    def open(self):
        """ client opened websocket    """
        print("WebSocket opened...")


    def on_message(self, message):
        """ dispatch by method """
        print("received: " +  str(message))
        data = json.loads(message)
        result = None
        try:   
            # get the method to call
            f = getattr(self, data.pop("method"), None)
            # check if its really a callable method
            if callable(f):
                # call the given method
                result = f(data)
            if result:
                #good => return the result
                self.write_message(result)
        # not good => return the error message                
        except Exception as e:
            data = {
                "method"    :   "dispatcher",
                "type"      :   "error",
                "data"      :   str(e)
            }
            self.write_message(json.dumps(data))
    
    
    def echo(self, message):
        """ send the echo reply       """
        
        data = {
                "method"    :   "echo",
                "type"      :   "message",
                "data"      :  json.dumps(message)
            }
        return json.dumps(data)
        
    def on_close(self):
        print("WebSocket closed")


