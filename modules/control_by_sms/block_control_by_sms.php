<script type="text/javascript">
function submitform()
{
	document.write("testando!");
 //   document.forms["myform"].submit();
hostname = "192.168.0.105"
port = "3435"
var conn = new TCPSocket(hostname, port)
 
conn.onopen = function() { alert('connection opened!') }
conn.onread = function(data) { alert('RECEIVE: ' + data) }
conn.onclose = function(data) { alert('connection closed!') }
 
conn.send('Hello World');
}
</script>


<?php
$con_timeout = 3;

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
		$schedule_sms.= '<html><body><br />';

		// First Service //
		$schedule_sms.= '<form name="schedule_sms" id="schedule_sms" action="send.php" method="post">';
		$schedule_sms.= '<div style="text-align:center;"><b>';
		$schedule_sms.= get_string('schedule_sms', 'block_control_by_sms');
                $schedule_sms.= '</b></div>';

		$schedule_sms.= '<table>';
		$schedule_sms.= '<tr><td>';
		$schedule_sms.= '<input type="text" name="message" value="" />';
		$schedule_sms.= '</td></tr>';

		$schedule_sms.= '<tr><td>';
		//$schedule_sms.= '<div style="text-align:center;"><input type="submit" name="Agendar!" value="Enviar" /><br /></div>';
		$schedule_sms.= '<a href="javascript: submitform()">Submit</a>';
		$schedule_sms.= '</td></tr>';

		$schedule_sms.= '</table>';
		$schedule_sms.= '</form>';

		// Tail //
                $schedule_sms.= "<br /></body></html>";

		$this->content->text   = $schedule_sms;
		$this->content->footer = 'Developed by Rozsa';
		
		return $this->content;
	}

	public function specialization() {
		$this->ping_daemon();
	}
	
/********************************/
/*      Private Functions 	*/
/********************************/

	private function ping_daemon() {

		global $CFG;

		if (empty($this->config->daemon_address)) {
			//$this->config->daemon_address = "127.0.0.1";
		}
		if (empty($this->config->daemon_port)) {
			$this->config->daemon_port = 3435;
		}

		//echo "$this->config->daemon_address";
		$stream = fsockopen("192.168.0.105", 3435, $errno, $errstr, $con_timeout);
		//stream_set_timeout($stream, $timeout);

		if ($stream == Null) {
			echo "Failed to connect to daemon.";
		} else {
			echo "Connected to daemon successful.";
		}
		fclose($stream);
		
	}
} 
