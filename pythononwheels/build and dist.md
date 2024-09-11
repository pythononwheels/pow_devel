# build and dist.


# build dist and wheel


python setup.py sdist bdist_wheel


## test locally
### example:

pip install ./dist/pythononwheels-0.925.54.tar.gz

## upload to pypi

twine upload dist/* 


