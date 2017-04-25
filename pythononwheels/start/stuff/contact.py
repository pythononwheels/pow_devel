#
# TinyDB Model:  Contact
#
from itest.models.tinydb.basemodel import TinyBaseModel

class Contact(TinyBaseModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # Remember: There are no "sql" or "sqltype" keyowrds
    # allowed since this is a TinyDB Model.
    #
    schema = {
        'email'         : {'type': 'string'},
        "domain"        : { "type" : "string" },
        'firstname'     : {'type': 'string', 'maxlength' : 55}, # from email_address
        'lastname'      : {'type': 'string', 'maxlength' : 55}, # from email_adress
        "emails_sent"       : { "type" : "integer" },           # just "caching" the num of emails in enronset from this account.
        "emails_received"   : { "type" : "integer" }            # just "caching" the num of emails in enronset from this account.
    }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
    @property
    def email_address(self):
        return self.email
    
    @email_address.setter
    def email_address(self, addr):
        """ automatically sets first and lastname as well """
        self.email = addr
        # also set the last and firstname
        self.domain = addr.split("@")[1]
        namepart = addr.split("@")[0]
        try:
            i = namepart.index(".")
            # has a dot, so splitting for first ´/ lastname
            self.firstname = namepart.split(".")[0]
            self.lastname = namepart.split(".")[1]
        except ValueError as e:
            # no "."" => assuming only lastname
            self.lastname = addr.split("@")[0]
