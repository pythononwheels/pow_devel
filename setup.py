from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pythononwheels",
    version="0.925.55",
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
            "src/*",
            "src/data/*",
            "src/log/*",
            "src/database/*",
            "src/conf/*",
            "src/lib/*",
            "src/handlers/*",
            "src/migrations/*",
            "src/migrations/versions/*",
            "src/models/*",
            "src/models/tinydb/*",
            "src/models/elastic/*",
            "src/models/sql/*",
            "src/models/mongodb/*",
            "src/models/redis/*",
            "src/static/*",
            "src/static/css/*",
            "src/static/css/highlight-styles/*",
            "src/static/css/spectre/*",
            "src/static/css/bs4/*",
            "src/static/css/bs5/*",
            "src/static/js/*",
            "src/static/js/bs4/*",
            "src/static/js/bs5/*",
            "src/static/images/*",
            "src/static/svg/*",
            "src/static/sui/*",
            "src/static/sui/components/*",
            "src/static/sui/themes/basic/assets/fonts/*",
            "src/static/sui/themes/default/assets/fonts/*",
            "src/static/sui/themes/default/assets/images/*",
            "src/static/sui/themes/github/assets/fonts/*",
            "src/static/sui/themes/material/assets/fonts/*",
            "src/static/sui/components/*",
            "src/static/sui/components/*",
            "src/static/sui/components/*",
            "src/stubs/*",
            "src/tests/*",
            "src/tools/*",
            "src/views/*",
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
