#
# Pow MongoDB Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest
import time

#
# MongoDB tests
#
@pytest.mark.run(order=1)
@pytest.mark.mongodb
def test_mongodb_generate_model(modelname):
    """ 
        test if MongoDB model is generated
    """
    print(" .. Test MongoDB generate_model")
    import {{appname}}.generate_model as gm
    import uuid
    import os.path
    ret = gm.generate_model(modelname, "mongodb", appname="{{appname}}")
    # generate model returns true in case of success
    assert ret is True
    assert os.path.exists(os.path.normpath("../models/mongodb/" + modelname + ".py"))
