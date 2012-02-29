<?php
	$con_timeout = 3;

	//echo "$this->config->daemon_address";
	$stream = fsockopen("192.168.0.105", 3435, $errno, $errstr, $con_timeout);
	//stream_set_timeout($stream, $timeout);
	
	if ($stream == Null) {
	        echo "Failed to connect to daemon.";
	} else {
	        echo "Connected to daemon successful.";
	}
	fclose($stream);

?>
