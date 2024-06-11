## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# config for Corporal web app
#
<%text>############################################################</%text>


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail.config]
include = %(here)s/rattail.conf

[tailbone]
expose_websockets = true


<%text>##############################</%text>
# pyramid
<%text>##############################</%text>

[app:main]
use = egg:Corporal

pyramid.reload_templates = false
pyramid.debug_all = false
pyramid.default_locale_name = en
pyramid.includes = pyramid_exclog

beaker.session.type = file
beaker.session.data_dir = %(here)s/sessions/data
beaker.session.lock_dir = %(here)s/sessions/lock
beaker.session.secret = ${env.tailbone_beaker_secret}
beaker.session.key = ${envname}

pyramid_deform.tempdir = %(here)s/data/uploads

exclog.extra_info = true

# required for tailbone
rattail.config = %(__file__)s


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[handler_file]
args = ('${envdir}/app/log/webasgi.log', 'a', 'utf_8')
