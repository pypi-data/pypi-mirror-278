#!/bin/sh -e

# NOTE: this script is meant be ran by the 'rattail' user!

if [ "$1" = "--verbose" ]; then
    VERBOSE='--verbose'
    QUIET=
else
    VERBOSE=
    QUIET='--quiet'
fi

SRC=${envdir}/src
PIP=${envdir}/bin/pip
export PIP_CONFIG_FILE=${envdir}/pip.conf

# upgrade pip and friends
$PIP install $QUIET --disable-pip-version-check --upgrade pip
$PIP install $QUIET --upgrade setuptools wheel

% if not production:
# update all source packages...

cd $SRC/pycorepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/rattail
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/rattail-corepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/tailbone
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/tailbone-corepos
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/rattail-fabric2
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

cd $SRC/corporal
git pull $QUIET
find . -name '*.pyc' -delete
$PIP install $QUIET --editable .

% endif

# upgrade all dependencies for Corporal
$PIP install $QUIET --upgrade --upgrade-strategy eager 'Corporal'

# migrate database schema
cd ${envdir}
bin/alembic --config app/rattail.conf upgrade heads
