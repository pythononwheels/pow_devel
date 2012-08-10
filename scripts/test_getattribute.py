class A(object):
    def __init__(self):
        self.__dict__['x'] = 5
        self.adict = {}
        

    def __getattribute__(self, name):
        if name != '__dict__':
            print '__getattribute__', name
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if name != '__dict__':
            print '__getattr__', name
        return 7

    def __setattr__(self, name, value):
        print '__setattr__', name, value
        return object.__setattr__(self, name, value)

    def func(self, x):
        return x+1
    
class B(object):
    
    def __inti__(self):
        super(B, self).__init__()
    def meths(self):
        return [method for method in dir(self) if callable(getattr(self, method))]
    def a(self):
        return
    def b(self):
        return
    
if __name__ == '__main__':
    a = A()
    a.y = 6
    print a.x
    print a.y
    print a.z
    print a.func(2)
    print a.adict
    print "B"
    b = B()
    b.meths()