class Foo:
    def __init__(self, x):
        self.x = x
       
    def bar(self, y):
        return self.x + y

def wrap(cls):
    for k, v in cls.__dict__.items():
        print "key,value:", k,v
        print "type v", type(v)
        print "type(wrap)", type(wrap)
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

foo = Foo(3)
wrap(Foo)
print foo.bar(4)