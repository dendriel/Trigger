<script type="text/javascript">
function schedule_sms()
{
	var load = window.open('/moodle/blocks/control_by_sms/schedule_sms.php','','scrollbars=no,menubar=no,height=600,width=800,resizable=no,toolbar=no,location=no,status=no');
}
function send_sms()
{
	var load = window.open('/moodle/blocks/control_by_sms/schedule_sms.php','','scrollbars=no,menubar=no,height=600,width=800,resizable=no,toolbar=no,location=no,status=no');
}
</script>


<?php

class block_control_by_sms extends block_base {

	public function init() {
		$this->title = get_string('control_by_sms', 'block_control_by_sms');
	}

	public function get_content() {
		if ($this->content !== null) {
			return $this->content;
		}
			
		$this->content         =  new stdClass;

		// Header //
                $header = "<html><body>";
		$schedule_sms.= '<html><body>';
		$schedule_sms.= '<table>';

		// First Service //
		$schedule_sms.= '<tr>';
		$schedule_sms.= '<div style="text-align:center;"><b>';
		$schedule_sms.= '<a href="javascript: schedule_sms()">';
		$schedule_sms.= get_string('schedule_sms', 'block_control_by_sms');
                $schedule_sms.= '</a></b></div>';
		$schedule_sms.= '</tr>';

		// Second Service //
		$schedule_sms.= '<tr>';
		$schedule_sms.= '<div style="text-align:center;"><b>';
		$schedule_sms.= '<a href="javascript: send_sms()">';
		$schedule_sms.= get_string('send_sms', 'block_control_by_sms');
                $schedule_sms.= '</a></b></div>';
		$schedule_sms.= '</tr>';


		$schedule_sms.= '</table>';

		// Tail //
                $schedule_sms.= "</body></html>";

		$this->content->text   = $schedule_sms;
		$this->content->footer = 'Developed by Rozsa';
		
		return $this->content;
	}

	public function specialization() {
		global $USER;
		$user = $USER->id;
		echo "dasda $user";
	
		//$this->ping_daemon();
	}
	
/********************************/
/*      Private Functions 	*/
/********************************/

	private function ping_daemon() {

		if (empty($this->config->daemon_address)) {
			//$this->config->daemon_address = "127.0.0.1";
		}
		if (empty($this->config->daemon_port)) {
			$this->config->daemon_port = 3435;
		}

	}
} 
