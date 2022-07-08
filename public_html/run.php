<?php
define("ADDRESS","127.0.0.1");
define("USER","pi");
define("PASSWORD","raspberry");

/* SSH2 module processes */
$sconnection = ssh2_connect(ADDRESS,22);
ssh2_auth_password($sconnection,USER,PASSWORD);
$command = "/usr/bin/sudo /usr/bin/python3 /home/pi/codes/give_candy.py";
$stdio_stream = ssh2_exec($sconnection,$command);
ssh2_disconnect($sconnection);
?>
