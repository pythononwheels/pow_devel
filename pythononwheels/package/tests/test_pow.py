#
# Pow Default Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest
import time
# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform



@pytest.mark.notonosx
@pytest.mark.run(order=1)
@pytest.mark.minimal
def test_server():
    """ test if server starts
        calls baseurl:port/test/12 
        must return 12.
        This test the server, routing and method dispatching
    """
    print(" .. Test if server works" )        
    from multiprocessing import Process
    import {{appname}}.server
    import requests
    import {{appname}}.conf.config as cfg
    import time
    p = Process(target={{appname}}.server.main)
    p.start()
    testurl=cfg.server_settings["protocol"] + cfg.server_settings["host"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  
    time.sleep(5)
    r = requests.get(testurl)
    p.terminate()
    assert int(r.text)==12


    
    
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
    

