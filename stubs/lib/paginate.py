#
# will_paginate helpder 
# khz / July 2012
#

class WilPaginate(list):
    
    def __init__(self):
        super(WillPaginate, self).__init__()
        self._count = 0
    
    def get_count():
        return self._count
    
    def set_count(val):
        self._count = val
 