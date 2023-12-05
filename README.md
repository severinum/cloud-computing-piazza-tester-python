# Test Package for PIAZZA Api (CW)

This test package was created using Python. It uses `pytest` library to test API

## Installing dependencies

To install Python dependencies for the test pack, run command:

`pip3 install -U requests Flask pytest pytest-html pyjwt`

Test if you can now run command `pytest`. If not, export it to system path with command `export PATH=/Users//Library/Python/3.8/bin:$PATH` Check your puthon version, in my case that was 3.8 but your path may be different if you have diferent python version. Update command accordingly.

## Running test suite

From the same location as test files, run command:

`pytest`

To get test report as custom named HTML file, run command:

`pytest -sv --html report.html`

