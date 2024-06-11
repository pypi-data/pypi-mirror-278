## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} Views
"""

from corporal.web.views import essentials


def includeme(config):

    # include all views deemed "essential" for Corporal
    essentials.defaults(config)

    # TODO: include more (e.g. custom) views here as needed
