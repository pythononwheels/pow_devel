#
#
# test method dispatching for olugins using getattr
#

class Validate(object):
    
    def __init__(self):
        pass
    
    def presence_of(self, model_attribute):
        print "validating the presence of an attribute: ", model_attribute
        return


class Model(object, Validate):
    
    
    def __init__(self):
        self.firstname = "None"
        self.lastname = "None"
    
    
    def set_firstname(self, name):
        self.firstname = name
        return

    def set_lastname(self, name):
        self.lastname = name
        return


if __name__ == "__main__":
    print "start test"