## -*- mode: conf; -*-

${envdir}/pip.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 rattail rattail
}

${envdir}/app/log/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 rattail rattail
}
