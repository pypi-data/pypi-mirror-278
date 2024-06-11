## -*- mode: conf; -*-

<%text>############################################################</%text>
#
# cron config for Corporal
#
<%text>############################################################</%text>


<%text>##############################</%text>
# rattail
<%text>##############################</%text>

[rattail.config]
include = %(here)s/rattail.conf


<%text>##############################</%text>
# alembic
<%text>##############################</%text>

[alembic]
script_location = corporal.db:alembic
version_locations = corporal.db:alembic/versions rattail.db:alembic/versions


<%text>##############################</%text>
# logging
<%text>##############################</%text>

[handler_console]
level = WARNING

[handler_file]
args = ('${envdir}/app/log/cron.log', 'a', 'utf_8')
