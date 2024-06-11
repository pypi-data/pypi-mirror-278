## -*- coding: utf-8; mode: php; -*-
<?php

class ${org_studly_prefix}DemoTask extends FannieTask
{
    public $name = "${organization} Demo";

    public $description = 'Demo command that tries to connect to
Tailbone API, and reports success/failure.

NOTE: This task is provided by the ${org_studly_prefix}Demo plugin;
please see that for settings to control behavior.';

    public $default_schedule = array(
        'min' => 0,
        'hour' => 5,
        'day' => '*',
        'month' => '*',
        'weekday' => '*',
    );

    public function run()
    {
        $this->cronMsg("hello from ${org_studly_prefix}Demo!", FannieLogger::INFO);

        % if use_posterior:

        $settings = $this->config->get('PLUGIN_SETTINGS');

        $url = $settings['PoserDemoTailboneAPIURL'];
        if (!$url) {
            $this->cronMsg("must define the Tailbone API URL", FannieLogger::ERROR);
            return;
        }

        $token = $settings['PoserDemoTailboneAPIToken'];
        if (!$token) {
            $this->cronMsg("must define the Tailbone API token", FannieLogger::ERROR);
            return;
        }

        $verifySSL = $settings['PoserDemoTailboneAPIVerifySSL'] === 'false' ? false : true;

        $posterior = new \Rattail\Posterior\Client($url, $token, $verifySSL);

        try {
            $response = $posterior->get('/about');
        } catch (Exception $e) {
            $this->cronMsg($e, FannieLogger::ERROR);
            return;
        }

        $body = $response->getBody();
        $this->cronMsg("response body was: $body", FannieLogger::INFO);
        print("$body\n");

        % else:

        $this->cronMsg("task is complete!", FannieLogger::INFO);
        print("task is complete!\n");

        % endif
    }
}
