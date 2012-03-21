<?php
include('./php/libs/IXR_Library.inc.php');

$DAEMON_ADDRESS = "192.168.0.105";
$DAEMON_PORT = 3435;

$server_address = 'http://' . $DAEMON_ADDRESS . ':' . $DAEMON_PORT . '/RPC2';

try {
    $client = new IXR_Client($server_address);
    
    if (! $client->query('systemHalt')) {
        print 'Procedure returned error message: ' . $client->getErrorMessage() . '.';
    }
    if ($client->getResponse() == 0) {
        echo "<br />Command Sent!";

    } else {
        echo "<br />Command Sent!";
    }
} catch (Exception $e) {
    echo "Failed to communicate with the server! $e";
}
?>
