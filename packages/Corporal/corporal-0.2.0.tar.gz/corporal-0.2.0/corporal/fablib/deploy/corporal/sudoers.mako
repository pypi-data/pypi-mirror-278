# -*- mode: conf; -*-

# let rattail upgrade the app
rattail ALL = NOPASSWD: ${envdir}/app/upgrade-wrapper.sh
rattail ALL = NOPASSWD: ${envdir}/app/upgrade-wrapper.sh --verbose

# # let rattail manage supervisor daemons
# rattail ALL = NOPASSWD: /usr/bin/supervisorctl stop ${safename}\:
# rattail ALL = NOPASSWD: /usr/bin/supervisorctl start ${safename}\:
