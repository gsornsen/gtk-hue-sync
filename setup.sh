#!/bin/bash -ei

CWD=$PWD

# Create virtual environment
if [ ! -d "env" ];then
    printf "\nCreating virtual environment\n"
    if [ $1 = 'travis' ];then
        echo "Travis Environment"
        make travis-env
    else
        make env
    fi
else
    printf "\nVirtual environment exists\n"
fi

# Source virtual environment
source env/bin/activate

# Install hue-python-rgb-converter python dependency
git clone https://github.com/benknight/hue-python-rgb-converter.git /tmp/hue-python-rgb-converter
cd /tmp/hue-python-rgb-converter
python setup.py install
cd $CWD
rm -rf /tmp/hue-python-rgb-converter


# Install forked color-thief python dependency
# TODO - Fix this if pull request ever gets approved
git clone https://github.com/gsornsen/color-thief-py.git /tmp/color-thief-py
cd /tmp/color-thief-py
python setup.py install
cd $CWD
rm -rf /tmp/color-thief-py

# Set-up yapf pre-commit hook
cp -rv git_hooks/pre-commit .git/hooks/pre-commit

echo $'\nSuccess! Please enter source env/bin/activate\n'