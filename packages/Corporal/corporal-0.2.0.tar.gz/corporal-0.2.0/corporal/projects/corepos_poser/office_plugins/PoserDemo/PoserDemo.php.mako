## -*- coding: utf-8; mode: php; -*-
<?php

class ${org_studly_prefix}Demo extends COREPOS\Fannie\API\FanniePlugin
{
    public $plugin_description = "Demo plugin for ${organization}";

    public $plugin_settings = [

    % if use_posterior:

        '${org_studly_prefix}DemoTailboneAPIURL' => [
            'label' => 'Tailbone API URL',
            'description' => 'Base URL for Tailbone API (usually ends with /api)',
        ],

        '${org_studly_prefix}DemoTailboneAPIToken' => [
            'label' => 'Tailbone API Token',
            'description' => 'User auth token for use with Tailbone API',
        ],

        '${org_studly_prefix}DemoTailboneAPIVerifySSL' => [
            'label' => 'Verify SSL',
            'description' => 'Validate SSL cert used by Tailbone API?',
            'options' => [
                "Yes, validate the SSL cert" => 'true',
                "No, do not validate the SSL cert (SHOULD ONLY BE USED FOR TESTING!)" => 'false',
            ],
            'default'=>'true',
        ],

    % else:

        '${org_studly_prefix}Foo' => [
            'label' => 'Foo',
            'description'=>'Some important foo setting',
            'default' => 'bar',
        ],

    % endif

    ];
}
