from optparse import OptionParser

class B(object):
    
    def __init__(self):
        super(B, self).__init__()
    def meths(self):
        import inspect
        alist =  inspect.getmembers(self, predicate=inspect.ismethod)
        for elem in alist:
            print elem[0]
      

    def a(self):
        print "I am a"
        
    def b(self):
        print "I am b"
    
if __name__ == '__main__':
    
    print "B"
    b = B()
    b.meths()