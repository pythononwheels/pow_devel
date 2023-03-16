from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

#setting __version__ from pythononwheels/version.py
exec(open(os.path.join(os.path.join(here, "pythononwheels"), "version.py")).read())

setup(
    name="pythononwheels",
    version=__version__,
    description="The simple, quick and easy generative web framework for python",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules ",
    ],
    keywords="framework web development",
    url="http://www.pythononwheels.org",
    author="khz",
    author_email="khz@tzi.org",
    license="MIT",
    packages=["pythononwheels"],
    package_dir={"pythononwheels": "pythononwheels"},
    package_data={
        "pythononwheels": [
            "package/*",
            "package/data/*",
            "package/log/*",
            "package/database/*",
            "package/conf/*",
            "package/lib/*",
            "package/handlers/*",
            "package/migrations/*",
            "package/migrations/versions/*",
            "package/models/*",
            "package/models/tinydb/*",
            "package/models/elastic/*",
            "package/models/sql/*",
            "package/models/mongodb/*",
            "package/models/redis/*",
            "package/static/*",
            "package/static/css/*",
            "package/static/css/highlight-styles/*",
            "package/static/css/spectre/*",
            "package/static/css/bs4/*",
            "package/static/css/bs5/*",
            "package/static/js/*",
            "package/static/js/bs4/*",
            "package/static/js/bs5/*",
            "package/static/images/*",
            "package/static/svg/*",
            "package/static/sui/*",
            "package/static/sui/components/*",
            "package/static/sui/themes/basic/assets/fonts/*",
            "package/static/sui/themes/default/assets/fonts/*",
            "package/static/sui/themes/default/assets/images/*",
            "package/static/sui/themes/github/assets/fonts/*",
            "package/static/sui/themes/material/assets/fonts/*",
            "package/static/sui/components/*",
            "package/static/sui/components/*",
            "package/static/sui/components/*",
            "package/stubs/*",
            "package/tests/*",
            "package/tools/*",
            "package/views/*",
            "./update_conf.py",
        ]
    },
    install_requires=["tornado"],
    entry_points={
        "console_scripts": [
            "generate_app = pythononwheels.generate_app:main",
        ]
    },
    # scripts=['bin/generate_app'],
    zip_safe=False,
)
