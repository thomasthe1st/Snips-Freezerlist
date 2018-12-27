#!/usr/bin/env bash -e

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python2`

    if [ ! -f ${PYTHON} ]
    then
        echo "could not find python"
    fi
    virtualenv -p ${PYTHON} ${VENV}

fi

. ${VENV}/bin/activate

pip install -r requirements.txt

if [ ! -f ./.shoppinglist ]; then
    touch .shoppinglist
    sudo chown _snips-skills .shoppinglist
fi

if [ ! -f config.ini ]
then
    cp config.ini.default config.ini
fi
