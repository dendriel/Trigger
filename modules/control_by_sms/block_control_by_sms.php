<?php

class block_control_by_sms extends block_base {

    public function init() 
    {
    	$this->title = get_string('control_by_sms', 'block_control_by_sms');
    }
    
    public function get_content() 
    {
    	if ($this->content !== null) {
            return $this->content;
    	}
    		
    	$this->content = new stdClass;
    
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
    
        // Third Service //
    	$schedule_sms.= '<tr>';
    	$schedule_sms.= '<div style="text-align:center;"><b>';
    	$schedule_sms.= '<a href="javascript: configure_feature()">';
        $schedule_sms.= 'Configure';
        $schedule_sms.= '</a></b></div>';
  	$schedule_sms.= '</tr>';
    
        // Fourth Service //
    	$schedule_sms.= '<tr>';
    	$schedule_sms.= '<div style="text-align:center;"><b>';
    	$schedule_sms.= '<a href="javascript: send_sms()">';
        $schedule_sms.= 'Reports';
        $schedule_sms.= '</a></b></div>';
  	$schedule_sms.= '</tr>';

    	$schedule_sms.= '</table>';
    
    	// Tail //
        $schedule_sms.= "</body></html>";
    
    	$this->content->text   = $schedule_sms;
    	$this->content->footer = 'Developed by Rozsa';
    	
    	return $this->content;
    }
    
    public function specialization() 
    {
    	global $COURSE;
        global $USER;

    	$course_id = $COURSE->id;
        $user_id = $USER->id;
    
    	$js.= "<script type=\"text/javascript\">\n";

    	$js.= "function schedule_sms() {\n";
    	$js.= "var load = window.open('/moodle/blocks/control_by_sms/schedule_sms.php?course_id=' + $course_id + '&user_id=' + $user_id,'','scrollbars=no,menubar=no,height=500,width=800,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.=  "}\n";

    	$js.= "function send_sms() {\n";
    	$js.= "var load = window.open('/moodle/blocks/control_by_sms/schedule_sms.php','','scrollbars=no,menubar=no,height=500,width=700,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.= "}\n";

        $js.= "function configure_feature() {\n";
        $js.= "var load = window.open('/moodle/blocks/control_by_sms/configure_sms.php','','scrollbars=no,menubar=no,height=500,width=800,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.= "}\n";

    	$js.= "</script>\n";
    
    	echo $js;

    }
	
/********************************/
/*      Private Functions 	*/
/********************************/

//	private function ping_daemon() {

//		if (empty($this->config->daemon_address)) {
			//$this->config->daemon_address = "127.0.0.1";
//		}
//		if (empty($this->config->daemon_port)) {
//			$this->config->daemon_port = 3435;
//		}

//	}
} 
