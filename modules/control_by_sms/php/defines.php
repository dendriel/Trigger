<?php
$DAEMON_ADDRESS = "192.168.0.105";
$DAEMON_PORT = 3435;
$server_address = 'http://' . $DAEMON_ADDRESS . ':' . $DAEMON_PORT . '/RPC2';

$OPERATOR = 0;
$TRUE = 0;

// REQUISITION STATUS //
$ACTIVE   = 0;
$CANCELED = 1;
$FAILED   = 2;
$SENT     = 3;

// Package types //
$ID    = 0;
$BLOW  = 1;
$ORIG  = 3;
$MSG   = 4;
$DESTN = 5;
?>
