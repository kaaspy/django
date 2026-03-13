#!/bin/bash

pip --version

#path.py was renamed to path and is pretty deprecated
#Which implies no dev branch to clone
#https://pypi.org/project/path/
#https://github.com/jaraco/path

[ -d "my_dir" ] && rm -rf "my_dir"
[ -d "local_lib" ] && rm -rf "local_lib"
mkdir "local_lib"
git clone "https://github.com/jaraco/path" "local_lib/source"
python -m pip install "local_lib/source" --target="local_lib" >install.log

[ -d "local_lib/path" ] && python my_program.py