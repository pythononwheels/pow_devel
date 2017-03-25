#
# Elastic Model:  Testelastic
#
from itest.models.elastic.basemodel import ElasticBaseModel
from itest.database.elasticdblib import dbname
from datetime import datetime
from dateutil import parser

class Elasticmail(ElasticBaseModel):
    #
    # Use the cerberus schema style 
    # which offer you an Elastic schema and
    # immediate validation with cerberus
    #

    schema = {
        'sender'        : { 'type': 'string' },
        'to'            : { 'type': 'string', 'maxlength' : 255 },
        'date'          : { 'type': 'date' },
        'subject'       : { 'type': 'string' },
        'year'          : { "type": 'integer' },
        'month'         : { "type": 'integer' },
        'week'          : { "type": 'integer' },
        'msg'           : { "type": 'string' }
    }

    #
    # your model's methods down here
    # (the two below are just examples from the elasticsearch_dsl py documentation)
    #

    def setup_from_msg(self, msg):
        """
            requires an email.parser msg. (see python email.parser)
        """
        f = msg.get("From", None)
        if f:
            self.sender = f
        date = msg.get("Date", None)
        if date:
            self.set_date(date)
        to = msg.get("To", None)
        if to:
            self.to = to
        subj = msg.get("Subject", None)
        if subj:
            self.subject = subj
        self.msg = str(msg)

        return self


    def set_date(self, date):
        """ 
            sets the date as datetime directly or from string 
            uses dateutil to guess the format if string given.

            also sets the fast access helpers yera, month, week
        """
        if isinstance(date,datetime):
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
        d["msg"] = "NA"
        return pformat(d,indent=+4)