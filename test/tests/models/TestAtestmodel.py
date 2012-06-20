#
#
# The test stub file for your model Unit-Test
# just a basic test added by default that will fail.
# Please change the Unit test for this Model according to your needs.
#
 

import sys,os
import unittest

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
import powlib

class Atestmodel(unittest.TestCase):
    def setUp(self):
        # Setup everything needed for the test (should be as few as possible)
        return
    
    def testFirst(self):
        # test 1st says: 1st specify and fail, then implement and pass.
        assert False
        return
    
    def tearDown(self):
        # cleanup everything  
        return
