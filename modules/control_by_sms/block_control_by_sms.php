<?php

class block_control_by_sms extends block_base {

	public function init() {
		$this->title = get_string('control_by_sms', 'block_control_by_sms')
	}

	public function get_content() {
		if ($this->content !== null) {
			return $this->content;
		}
			
		$this->content         =  new stdClass;
		$this->content->text   = 'The content of our SimpleHTML block!';
		$this->content->footer = 'Footer here...';
		
		return $this->content;
	}
} 
