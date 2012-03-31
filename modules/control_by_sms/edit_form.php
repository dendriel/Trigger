<?php

class block_control_by_sms_edit_form extends block_edit_form {

	protected function specific_definition($mform) {

		// Section header title according to language file.
	        $mform->addElement('header', 'configheader', get_string('blocksettings', 'block'));

		// Daemon communication configurations.
		#$mform->addElement('static', 'description', get_string('daemon_configuration', 'block_control_by_sms'));
	       # $mform->addElement('advcheckbox', 'config_open_to_use', get_string('allow_to_use', 'block_control_by_sms'));
               #$mform->addElement('text', 'config_open_to_use', 'Text field (disabled default)');
               # $mform->disabledIf('config_open_to_use', 'advcheck');

                #$this->add_action_buttons(true);



	}
}
