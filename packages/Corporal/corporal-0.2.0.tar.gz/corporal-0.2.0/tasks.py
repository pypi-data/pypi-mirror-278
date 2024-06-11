# -*- coding: utf-8; -*-
"""
Tasks for Corporal
"""

import os
import shutil

from invoke import task


@task
def release(c):
    """
    Release a new version of Corporal
    """
    # rebuild package
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('Corporal.egg-info'):
        shutil.rmtree('Corporal.egg-info')
    c.run('python -m build --sdist')

    # upload to public PyPI
    c.run('twine upload dist/*')
