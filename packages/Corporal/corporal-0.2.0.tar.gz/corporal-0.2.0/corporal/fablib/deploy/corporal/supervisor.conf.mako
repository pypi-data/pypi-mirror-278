## -*- mode: conf; -*-

[group:${safename}]
programs=${safename}_webmain

[program:${safename}_webmain]
% if asgi:
environment=TAILBONE_ASGI_CONFIG="${envdir}/app/webasgi.conf"
command=${envdir}/bin/uvicorn --port ${port} --factory corporal.web.app:asgi_main
% else:
command=${envdir}/bin/pserve pastedeploy+ini:${envdir}/app/web.conf
directory=${envdir}/app/work
% endif
user=rattail
autostart=${'true' if autostart else 'false'}
