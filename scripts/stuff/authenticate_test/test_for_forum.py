class Foo:
    def __init__(self, x):
        self.x = x
        
    def bar(self, y):
        return self.x + y

    
class Protector(object):
    def __init__(self):
        self.to_protect = {}

    def pre(self): 
        print 'pre'
    
    def post(self): 
        print 'post'
    
    def wrap(self,cls):
        print cls.__dict__.items()
        for k, v in cls.__dict__.items():
            print "key, value:", k,v
            print "type self(wrap):", type(self.wrap)
            print "type(v):", type(v)
            if not k.startswith("__") and isinstance(v, type(self.wrap)):
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
    p.wrap(Foo)
    print foo.bar(4)
    