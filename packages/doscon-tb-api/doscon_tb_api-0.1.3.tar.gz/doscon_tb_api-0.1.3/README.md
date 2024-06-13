# tb_api
Library for connecting to thingsboard to perform API actions. 

# TESTS
requires<br>
pytest==7.4.4<br>
pytest-cov==4.1.0<br>

## To run tests
pytest


## How to build
pip install setuptools wheel<br>

python setup.py sdist bdist_wheel<br>

### upload to pipy
pip install twine<br>
twine upload dist/*<br>