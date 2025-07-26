# get-pip.py bootstrap script
# Downloaded from https://bootstrap.pypa.io/get-pip.py
# Run with: python get-pip.py

import urllib.request
exec(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py').read())
