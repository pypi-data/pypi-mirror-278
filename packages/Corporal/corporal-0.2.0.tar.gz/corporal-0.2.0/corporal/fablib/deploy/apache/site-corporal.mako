# -*- mode: apache; -*-

<VirtualHost *:80>
    ServerName ${sitename}

    # Corporal
    <Location "/">
        ProxyPreserveHost On
        ProxyPass "http://127.0.0.1:${port}/"
        ProxyPassReverse "http://127.0.0.1:${port}/"
    </Location>
    % if asgi:
    <Location "/ws/">
        ProxyPreserveHost On
        ProxyPass "ws://127.0.0.1:${port}/ws/"
        ProxyPassReverse "ws://127.0.0.1:${port}/ws/"
    </Location>
    % endif

    ErrorLog ${'$'}{APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${'$'}{APACHE_LOG_DIR}/access.log combined
</VirtualHost>
