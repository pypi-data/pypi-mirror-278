# -*- coding: utf-8; -*-
"""
Development Tasks for Corporal
"""

import os
import configparser
import shutil
import sys

from invoke import task
from sphinx.util.console import bold
from sphinx.cmd.quickstart import do_prompt

from bootstrap import inside_virtualenv


here = os.path.abspath(os.path.dirname(__file__))


@task
def bootstrap(c):
    """
    Bootstrap a development environment.
    """
    if not inside_virtualenv():
        sys.exit(1)

    envdir = sys.prefix
    upgrade_pip(c)
    install_app_package(c)
    appdir = make_appdir(c, envdir)

    info = collect_info()
    make_configs(c, envdir, appdir, info)
    check_db(c, envdir, appdir)
    install_db_schema(c, envdir, appdir)
    make_admin_user(c, envdir, appdir, info)

    print()
    print(bold("============================================================"))
    print()
    print(bold("  Okay, you should be ready to go!"))
    print()
    print(bold("============================================================"))
    print()
    print("start your development web app with this command:")
    print()
    print("    cd {}".format(envdir))
    if sys.platform == 'win32':
        print(r"    Scripts\pserve --reload file+ini:app\web.conf")
    else:
        print("    bin/pserve --reload file+ini:app/web.conf")
    print()
    print("then check out your development web app at:")
    print()
    print("    http://localhost:9080")
    print()


def collect_info():
    """
    Collect misc. dev info from user
    """
    info = {}
    print()
    print(bold("Welcome to Corporal, the CORE supplement."))

    config = configparser.ConfigParser()
    if config.read(os.path.join(here, 'settings.ini')):
        if config.has_section('devbootstrap'):
            info = dict(config.items('devbootstrap'))

    try:
        print()
        print("Please enter the details for your Corporal database.")
        print()
        info['dbhost'] = do_prompt('DB host',
                                   default=info.get('dbhost', 'localhost'))
        info['dbname'] = do_prompt('DB name',
                                   default=info.get('dbname', 'corporal'))
        info['dbuser'] = do_prompt('DB user',
                                   default=info.get('dbuser', 'rattail'))
        info['dbpass'] = do_prompt('DB password',
                                   default=info.get('dbpass'))

        print()
        print("Please enter the details for your Corporal admin user.")
        print()
        info['corporaluser'] = do_prompt('Corporal username',
                                     default=info.get('corporaluser', 'admin'))
        info['corporalpass'] = do_prompt('Corporal password',
                                     default=info.get('corporalpass'))

    except (KeyboardInterrupt, EOFError):
        print("\n[Interrupted.]")
        sys.exit(130)  # 128 + SIGINT

    return info


def upgrade_pip(c):
    """
    Upgrade pip and friends
    """
    if sys.platform == 'win32':
        c.run('python -m pip install -U pip')
    else:
        c.run('pip install -U pip')
    c.run('pip install -U setuptools wheel')


def install_app_package(c):
    """
    Install the Corporal app package
    """
    project = os.path.abspath(os.path.join(here, os.pardir))
    c.run('pip install -e {}'.format(project))
    # c.run('pip install Corporal')


def make_appdir(c, envdir):
    """
    Create the 'app' dir for virtual env
    """
    appdir = os.path.join(envdir, 'app')
    if not os.path.exists(appdir):
        if sys.platform == 'win32':
            c.run('{} make-appdir --path {}'.format(
                os.path.join(envdir, 'Scripts', 'rattail'),
                appdir))
        else:
            c.run('{}/bin/rattail make-appdir --path {}'.format(
                envdir, appdir))
    return appdir


def make_configs(c, envdir, appdir, info):
    """
    Create app config files
    """
    # rattail.conf
    if not os.path.exists(os.path.join(appdir, 'rattail.conf')):
        with open('rattail.conf') as f:
            contents = f.read()
        contents = contents.replace('<ENVDIR>', envdir)
        contents = contents.replace('<SEP>', os.sep)
        contents = contents.replace('<DBHOST>', info['dbhost'])
        contents = contents.replace('<DBNAME>', info['dbname'])
        contents = contents.replace('<DBUSER>', info['dbuser'])
        contents = contents.replace('<DBPASS>', info['dbpass'])
        with open(os.path.join(appdir, 'rattail.conf'), 'w') as f:
            f.write(contents)

    # quiet.conf
    if not os.path.exists(os.path.join(appdir, 'quiet.conf')):
        if sys.platform == 'win32':
            c.run('{} make-config -T quiet -O {}'.format(
                  os.path.join(envdir, 'Scripts', 'rattail'),
                  appdir))
        else:
            c.run('{}/bin/rattail make-config -T quiet -O {}'.format(
                envdir, appdir))

    # web.conf
    if not os.path.exists(os.path.join(appdir, 'web.conf')):
        with open('web.conf') as f:
            contents = f.read()
        contents = contents.replace('<ENVDIR>', envdir)
        contents = contents.replace('<SEP>', os.sep)
        with open(os.path.join(appdir, 'web.conf'), 'w') as f:
            f.write(contents)


def check_db(c, envdir, appdir):
    """
    Do basic sanity checks for Corporal database
    """
    if sys.platform == 'win32':
        c.run('{} -c {} --no-versioning checkdb'.format(
              os.path.join(envdir, 'Scripts', 'rattail'),
              os.path.join(appdir, 'quiet.conf')))
    else:
        c.run('{}/bin/rattail -c {}/quiet.conf --no-versioning checkdb'.format(
            envdir, appdir))


def install_db_schema(c, envdir, appdir):
    """
    Install the schema for Corporal database
    """
    if sys.platform == 'win32':
        c.run('{} -c {} upgrade heads'.format(
              os.path.join(envdir, 'Scripts', 'alembic'),
              os.path.join(appdir, 'rattail.conf')))
    else:
        c.run('{}/bin/alembic -c {}/rattail.conf upgrade heads'.format(
            envdir, appdir))


def make_admin_user(c, envdir, appdir, info):
    """
    Make an admin user in the Corporal database
    """
    if sys.platform == 'win32':
        c.run('{} -c {} make-user --admin {} --password {}'.format(
              os.path.join(envdir, 'Scripts', 'rattail'),
              os.path.join(appdir, 'quiet.conf'),
              info['corporaluser'], info['corporalpass']))
    else:
        c.run('{}/bin/rattail -c {}/quiet.conf make-user --admin {} --password {}'.format(
            envdir, appdir, info['corporaluser'], info['corporalpass']))
