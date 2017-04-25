#
# TinyDB Model:  Email
#
from itest.models.tinydb.basemodel import TinyBaseModel
from dateutil import parser
import datetime

class Email(TinyBaseModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # Remember: There are no "sql" or "sqltype" keyowrds
    # allowed since this is a TinyDB Model.
    #
    schema = {
        '_from': {'type': 'string'},
        'from_contact_id': {'type': 'string'}, # uuid of the contact
        'date': {'type': "datetime" },
        "week" : { "type" : "integer"}, # just for faster access
        "year" : { "type" : "integer"}, # just for faster access
        "month" : { "type" : "integer"}, # just for faster access
        "to"    : {"type" : "string"},
        "to_contact_id" : {"type" : "string"}, # uuid of the contact
        "subject"   : { "type" : "string"},
        "msg" : { "type" : "string" },
        "raw_msg" : { "type" : "string" }
    }
    
    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
    def setup_from_msg(self, msg):
        """
            requires an email.parser msg. (see python email.parser)
        """
        f = msg.get("From", None)
        if f:
            self._from = f
        date = msg.get("Date", None)
        if date:
            self.set_date(date)
        to = msg.get("To", None)
        if to:
            self.to = to
        subj = msg.get("Subject", None)
        if subj:
            self.subject = subj
        self.raw_msg = str(msg)

        return self


    def set_date(self, date):
        """ 
            sets the date as datetime directly or from string 
            uses dateutil to guess the format if string given.

            also sets the fast access helpers yera, month, week
        """
        if isinstance(date,datetime.datetime):
            self.date = date
        elif isinstance(date, str):
            try:
                dt = parser.parse(date)     # use dateutil parser 
                self.date = dt
            except Exception as e:
                raise 
        else:
            raise TypeError("date must be of type: datetime.datetime or string")
        self.week = self.date.isocalendar()[1]
        self.year = self.date.year
        self.month = self.date.month

    def __repr__(self):
        #
        # __repr__ method is what happens when you look at it with the interactive prompt
        # or (unlikely: use the builtin repr() function)
        # usage: at interactive python prompt
        # p=Post()
        # p
        from pprint import pformat
        d = self.to_dict()
        d["raw_msg"] = "NA"
        return pformat(d,indent=+4)



