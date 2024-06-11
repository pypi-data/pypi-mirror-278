## -*- coding: utf-8; mode: js; -*-
{
    "name": "${org_slug}/poser",
    "description": "CORE-POS customizations for ${organization}",
    "require": {
        <% count = len(requires) %>
        % for i, pkg in enumerate(requires, 1):
        <% package, version = pkg %>
        "${package}": "${version}"${'' if i == count else ','}
        % endfor
    },
    "extra": {
        "merge-plugin": {
            "require": [
                "../IS4C/composer.json"
            ]
        }
    },
    "config": {
        "component-dir": "../IS4C/fannie/src/javascript/composer-components",
        "vendor-dir": "../IS4C/vendor",
        "allow-plugins": {
            "composer/installers": true,
            "oomphinc/composer-installers-extender": true,
            "corepos/composer-installer": true,
            "wikimedia/composer-merge-plugin": true
        }
    }
}
