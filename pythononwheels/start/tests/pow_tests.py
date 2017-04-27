#
# Pow Default Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest

# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform

MODELNAME = "pow_test_model"
class TestClass:
    @pytest.mark.notonosx
    def test_server(self):
        """ test if server starts
            calls baseurl:pot/test/12 
            must return 12.
            This test the server, routing and method dispatching
        """
        from multiprocessing import Process
        import {{appname}}.server
        import requests
        import {{appname}}.config as cfg
        import time
        p = Process(target={{appname}}.server.main)
        p.start()
        testurl=cfg.server_settings["base_url"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  
        r = requests.get(testurl)
        p.terminate()
        assert int(r.text)==12
        
    def test_generate_model(self):
        """ test if sql model is generated"""
        import {{appname}}.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "sql", appname="{{appname}}")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/sql/" + MODELNAME + ".py"))

    def test_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from {{appname}}.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)

    def test_sql_dbsetup(self):
        """ test the setup of the alembic environment """
        import {{appname}}.init_migrations
        import os
        os.chdir("..")
        r = {{appname}}.init_migrations.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    def test_sql_migration(self):
        """ test the setup of the alembic environment """
        import test.generate_migration
        import os
        os.chdir("..")
        script = test.generate_migration.generate_migration(message="pow_test")
        assert os.path.exists(os.path.normpath(script.path))

    def test_model_insert(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from {{appname}}.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        m.name = "Testname"
        
        assert isinstance(m, PowTestModel)


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
    

