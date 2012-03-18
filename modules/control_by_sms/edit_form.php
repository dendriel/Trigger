<?php

class block_control_by_sms_edit_form extends block_edit_form {

	protected function specific_definition($mform) {

		// Section header title according to language file.
	        $mform->addElement('header', 'configheader', get_string('blocksettings', 'block'));

		// Daemon communication configurations.
		$mform->addElement('static', 'description', get_string('daemon_configuration', 'block_control_by_sms'));

	        $mform->addElement('text', 'config_daemon_address', get_string('address', 'block_control_by_sms'));
	        $mform->setDefault('config_daemon_address', '127.0.0.1');
	        $mform->setType('config_daemon_address', PARAM_MULTILANG);       

	        $mform->addElement('text', 'config_daemon_port', get_string('port', 'block_control_by_sms'));
	        $mform->setDefault('config_daemon_port', '3435');
	        $mform->setType('config_daemon_port', PARAM_MULTILANG);       
	}
}
