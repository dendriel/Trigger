<?php

$settings->add(new admin_setting_heading(
            'headerconfig',
            get_string('headerconfig', 'block_control_by_sms'),
            get_string('descconfig', 'block_control_by_sms')
        ));
 
$settings->add(new admin_setting_configcheckbox(
            'control_by_sms/Allow_HTML',
            get_string('labelallowhtml', 'block_control_by_sms'),
            get_string('descallowhtml', 'block_control_by_sms'),
            '1'
        ));
