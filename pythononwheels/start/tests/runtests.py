#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest

# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform


if __name__ == "__main__":
    
    print(55*"-")
    print(" running pow Tests on: " + sys.platform)
    print(" ... ")
    if sys.platform.startswith("darwin"):
        # osx
        ret = pytest.main(["-k-notonosx", "pow_tests.py"])
    else:
        ret = pytest.main(["pow_tests.py"])
    
    print(" Failures: " +str(ret))
    print(55*"-")
    

