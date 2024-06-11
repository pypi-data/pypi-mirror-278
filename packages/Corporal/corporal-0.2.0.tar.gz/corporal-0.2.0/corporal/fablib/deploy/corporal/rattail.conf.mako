## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# base config for Corporal
#
<%text>############################################################</%text>


[corepos]
% if core_office_url:
office.url = ${core_office_url}
% endif

[corepos.db.office_op]
default.url = mysql+mysqlconnector://${env.username_mysql_coreserver}:${env.password_mysql_coreserver}@localhost/core_op
default.pool_recycle = 3600

[corepos.db.lane_op]
keys = ${', '.join([lane['dbkey'] for lane in lanes])}
% for lane in lanes:

${lane['dbkey']}.url = mysql+mysqlconnector://${lane['user']}:${lane['pw']}@${lane['host']}/${lane['op']}
% endfor


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail]
production = ${'true' if production else 'false'}
app_title = Corporal
appdir = ${envdir}/app
datadir = ${envdir}/app/data
workdir = ${envdir}/app/work
batch.files = ${envdir}/app/batch
export.files = ${envdir}/app/data/exports
runas.default = corporal

[rattail.config]
include = /etc/rattail/rattail.conf
usedb = true
preferdb = true

[rattail.db]
versioning.enabled = true
default.url = postgresql://rattail:${env.password_postgresql_rattail}@localhost/${dbname}
default.pool_pre_ping = true

[rattail.mail]
# this is the master switch, *no* emails are sent if false
send_emails = true

templates =
    corporal:templates/mail
    rattail:templates/mail

default.prefix = [Corporal]
#default.enabled = false

[rattail.upgrades]
command = sudo ${envdir}/app/upgrade-wrapper.sh --verbose
files = ${envdir}/app/data/upgrades


<%text>##############################</%text>
# alembic
<%text>##############################</%text>

[alembic]
script_location = rattail.db:alembic
version_locations = rattail_corepos.db:alembic/versions rattail.db:alembic/versions


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[handler_file]
args = ('${envdir}/app/log/rattail.log', 'a', 'utf_8')

[handler_email]
args = ('localhost', '${env.email_default_sender}', ${env.email_default_recipients}, "[Corporal] Logging")
