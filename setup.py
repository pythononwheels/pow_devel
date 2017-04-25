from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pythononwheels',
      version='0.5.21b',
      description='The simple, quick and easy generative web framework for python',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules ",
      ],
      keywords='framework web development',
      url='http://www.pythononwheels.org',
      author='khz',
      author_email='khz@tzi.org',
      license='MIT',
      packages=['pythononwheels'],
      package_dir={'pythononwheels': 'pythononwheels'},
      package_data={'pythononwheels': [
            'start/*',
            "start/database/*",
            "start/handlers/*",
            "start/migrations/*",
            "start/migrations/versions/*",
            "start/models/*", 
            "start/models/tinydb/*",
            "start/models/elastic/*",
            "start/models/sql/*",
            "start/static/*",
            "start/static/css/*",
            "start/static/js/*",
            "start/static/images/*",
            "start/static/svg/*",
            "start/stubs/*",
            "start/tests/*",
        ]},
      install_requires=[
        #"tornado>=4"
      ],
      entry_points={
        'console_scripts': [
            'pow_generate_app = pythononwheels.generate_app:main',
        ]
      },
      #scripts=['bin/generate_app'],
      zip_safe=False)