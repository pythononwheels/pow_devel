#
# define fixtures available for all testfiles here
# these can also rely on Databases 
#
import pytest


# sample, see: https://www.tutorialspoint.com/pytest/pytest_conftest_py.htm
@pytest.fixture
def modelname():
   return "pow_test_model"