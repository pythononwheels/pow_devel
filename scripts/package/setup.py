#
#
# Setup.py file for building a distribution pakage for PyPi
# 
# Status    : Test 
# Author    : khz@pythononwheels.org
# Date      : 10 / 09 / 2012
# manual    : http://packages.python.org/distribute/setuptools.html#using-find-packages
# PyPi info : http://getpython3.com/diveintopython3/packaging.html
# install   : http://www.pip-installer.org/en/latest/usage.html

from setuptools import setup, find_packages
setup(name='pythononwheels', 
      version='0.5.1dev',
      install_requires=[
                "SQLAlchemy", 
                "Beaker", 
                "Mako", 
                "nose", 
                "webob"
        ],
      # packages=find_packages(), -- should also work since:
      # find_packages will look for every directory containing a __init__.py file and include it.
       # But I will first try with the handcrafted approach ;) (khz/2012)
      packages=["pow_devel", 
                "pow_devel.stubs",
                "pow_devel.stubs.config",
                "pow_devel.stubs.controllers",
                "pow_devel.stubs.ext.auth",
                "pow_devel.stubs.ext.validate",
                "pow_devel.stubs.lib",
                "pow_devel.stubs.migrations",
                "pow_devel.stubs.partials"
                ],
      include_package_data=True,
      #metadata for upload to PyPI
      author = "khz",
      author_email = "khz@pythononwheels.org",
      description = "PyhtonOnWheels PyPi dist package",
      long_description = open('README').read(),
      license = "Licensed under the Apache License, Version 2.0",
      keywords = ["pythononwheels", "pow", "web", "framework", "generative", "wsgi", "simple", "small", "wsgi-framework"],
      url = "http://www.pythononwheels.org/",   
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: Pre-Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: APACHE 2.0",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        ],
      
      )
      