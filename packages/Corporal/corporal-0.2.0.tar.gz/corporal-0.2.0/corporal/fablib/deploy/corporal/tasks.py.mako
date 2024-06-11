## -*- mode: python; -*-
# -*- coding: utf-8; -*-

from invoke import task


@task
def upgrade(c):
    c.run('${envdir}/app/upgrade.sh --verbose')
