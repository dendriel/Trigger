<?php

/*$settings->add(new admin_setting_heading(
            'headerconfig',
            get_string('headerconfig', 'block_control_by_sms'),
            get_string('descconfig', 'block_control_by_sms')
        ));
*/
$settings->add(new admin_setting_configcheckbox(
            'control_by_sms/Open_to_use',
            get_string('label_open_to_use', 'block_control_by_sms'),
            get_string('desc_open_to_use', 'block_control_by_sms'),
            '1'
        ));
