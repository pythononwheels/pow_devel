class Wrapper(object):
    def __init__(self, obj):
        self.obj = obj
        
    def __getattr__(self, name):
        func = getattr(self.__dict__['obj'], name)
        if callable(func):
            def my_wrapper(*args, **kwargs):
                print "entering"
                ret = func(*args, **kwargs)
                print "exiting"
                return ret
            return my_wrapper
        else:
            return func
    

## for example on a string:
s = 'abc'
w = Wrapper(s)
print w.isdigit()