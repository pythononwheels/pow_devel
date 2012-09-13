class Foo:
    def __init__(self, x):
        self.x = x
        
    def bar(self, y):
        return self.x + y

def wrap(cls):
    print cls, type(cls)
    for k, v in cls.__dict__.items():
        print k
        if not k.startswith("__") and isinstance(v, type(wrap)):
            print "wrap", k
            setattr(cls, k, mkwrapper(v))
    
def mkwrapper(f):
    def wrapper(*args, **kwargs):
        print "vor ", f.__name__
        result = f(*args, **kwargs)
        print "nach", f.__name__
        return result
    return wrapper
    
class Protector(object):
    def __init__(self):
        self.to_protect = {}

    def pre(self): 
        print 'pre'
    
    def post(self): 
        print 'post'
    
    def wrap_old(self,cls):
        print type(self.wrap_old)
        print type(self.__class__.wrap_old)
        print cls.__dict__.items()
        for k, v in cls.__dict__.items():
            print "key, value:", k,v
            if not k.startswith("__") and isinstance(v, type(self.__class__.wrap_old)):
                print "wrap", k
                setattr(cls, k, mkwrapper(v))
                
    def wrap(self, instance):
        #print self.__dict__
        #print dir(self.__class__.__dict__)
        print instance.__class__.__dict__.items()
        for k, v in instance.__class__.__dict__.items():
            print k,v
            if not k.startswith("__"):
                func = getattr(instance, k)
                print "callable",callable(func)
                print "wrap", k
                setattr(instance.__class__, k, mkwrapper(v))
    
    def wrap_class(self, cls):
        #print self.__dict__
        #print dir(self.__class__.__dict__)
        print cls.__dict__.items()
        for k, v in cls.__dict__.items():
            print "key, value:", k,v
            if not k.startswith("__"):
                func = getattr(cls, k)
                print "callable",callable(func)
                print "wrap", k
                setattr(cls, k, mkwrapper(v))
    
    def mkwrapper(f):
        def wrapper(*args, **kwargs):
            print "vor ", f.__name__
            result = f(*args, **kwargs)
            print "nach", f.__name__
            return result
        return wrapper



if __name__ == "__main__":
    
    foo = Foo(3)
    p = Protector()
    #p.wrap(foo)
    #p.wrap_class(Foo)
    p.wrap_old(Foo)
    print foo.bar(4)
    print "----------------------"
    # 
    #wrap(Foo)
    #print foo.bar(4)