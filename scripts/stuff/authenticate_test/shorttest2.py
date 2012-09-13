#
# mostly taken from: http://www.semicomplete.com/blog/geekery/python-method-call-wrapper.html
#
class Filter(object):
    @staticmethod
    def wrapmethod(func, premethod=None, postmethod=None):
      def w(function, *args, **kwds):
        if premethod:
          premethod(*args, **kwds)
        function(*args, **kwds)
        if postmethod:
          postmethod(*args, **kwds)
      return lambda *x,**k: w(func,*x,**k)




def pre(self, *args, **kwds):
  print "hello: %s, %s" % (args, kwds)

def post(self, *args, **kwds):
  print "world: %s, %s" % (args, kwds)

class C(object):
    @staticmethod
    def pre(self, *args, **kwds):
        print "hello C: %s, %s" % (args, kwds)
    @staticmethod
    def post(self, *args, **kwds):
        print "world C: %s, %s" % (args, kwds)
    
  
class X(object):
    def Foo(self, *args, **kwds):
        try:
            print kwds['somearg']
        except: 
            print "No 'somearg' argument given"
    Foo = Filter.wrapmethod(Foo, C.pre)

x = X()

x.Foo(42, bar=33)
x.Foo(somearg="Hello there")
