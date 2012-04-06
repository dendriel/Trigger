<?php

class block_control_by_sms extends block_base {

    public function init() 
    {
    	$this->title = get_string('control_by_sms', 'block_control_by_sms');
    }

    function has_config() {
        return true;
    }
    
    public function get_content() 
    {
    	if ($this->content !== null) {
            return $this->content;
    	}

    	$this->content = new stdClass;
        $open_to_use = get_config('control_by_sms', 'Open_to_use');
        global $USER;

        $content.= "<html><body>";

        $schedule_sms.= '<table>';

        if($open_to_use) {
            // Schedule //
            $schedule_sms.= '<tr>';
            $schedule_sms.= '<div style="text-align:center;"><b>';
            $schedule_sms.= '<a href="javascript: schedule_sms()">';
            $schedule_sms.= get_string('schedule_sms_menu', 'block_control_by_sms');
            $schedule_sms.= '</a></b></div>';
            $schedule_sms.= '</tr>';
            // Reports //
            $schedule_sms.= '<tr>';
            $schedule_sms.= '<div style="text-align:center;"><b>';
            $schedule_sms.= '<a href="javascript: open_reports()">';
            $schedule_sms.= get_string('reports_menu', 'block_control_by_sms');
            $schedule_sms.= '</a></b></div>';
            $schedule_sms.= '</tr>';
    
            // Configure //   
/*            $schedule_sms.= '<tr>';
            $schedule_sms.= '<div style="text-align:center;"><b>';
            $schedule_sms.= '<a href="javascript: configure_feature()">';
            $schedule_sms.= 'Configure';
            $schedule_sms.= '</a></b></div>';
            $schedule_sms.= '</tr>';
*/
        } else {
            $schedule_sms.= '<tr>';
            $schedule_sms.= '<div style="text-align:center;"><b>';
            $schedule_sms.= '<a>';
            $schedule_sms.= get_string('service_stopped', 'block_control_by_sms');
            $schedule_sms.= '</a></b></div>';
            $schedule_sms.= '</tr>';
        }
        #$schedule_sms.= print_object($USER);
        $schedule_sms.= '</table>';
        $content.= $schedule_sms;
        $content.= '</body></html>';

    	$this->content->text   = $content;
    	$this->content->footer = get_string('footnote', 'block_control_by_sms');
    	
    	return $this->content;
    }
    
    public function specialization() 
    {
    	global $COURSE;
        global $USER;
        $w_height = 500;
        $w_width = 600;

        $w_height_r = 500;
        $w_width_r = 830;

    	$course_id = $COURSE->id;
        $user_id = $USER->id;

        $req_type = 0; //TODO find a way to get variables from ./php/defines,php and use the $ACTIVE macro.
    
    	$js.= "<script type=\"text/javascript\">\n";

    	$js.= "function schedule_sms() {\n";
    	$js.= "window.open('/moodle/blocks/control_by_sms/schedule_sms.php?course_id=$course_id&user_id=$user_id','','scrollbars=no,menubar=no,height=$w_height,width=$w_width,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.=  "}\n";

        $js.= "function configure_feature() {\n";
        $js.= "window.open('/moodle/blocks/control_by_sms/configure_sms.php','','scrollbars=no,menubar=no,height=500,width=800,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.= "}\n";

    	$js.= "function open_reports() {\n";
    	$js.= "window.open('/moodle/blocks/control_by_sms/reports.php?req_type=$req_type&user_id=$user_id','','scrollbars=no,menubar=no,height=$w_height_r,width=$w_width_r,resizable=no,toolbar=no,location=no,status=no'); \n";
        $js.= "}\n";

    	$js.= "</script>\n";
    
    	echo $js;

    }
} 
