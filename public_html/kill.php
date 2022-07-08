<?php
define("ADDRESS","127.0.0.1");
define("USER","pi");
define("PASSWORD","raspberry");


/* SSH2 module processes */
$sconnection = ssh2_connect(ADDRESS,22);
ssh2_auth_password($sconnection,USER,PASSWORD);

//ファイル読む
$MCjson = file_get_contents("/home/pi/system_pid.log");
echo $MCjson;

//kill
$command = "/usr/bin/sudo /usr/bin/kill ".$MCjson;
ssh2_exec($sconnection,$command);
$command = "/usr/bin/echo '' > /home/pi/system_pid.log";
ssh2_exec($sconnection,$command);


// 音楽の停止
$command = "/usr/bin/sudo /home/pi/codes/stop_allmusic.sh";
ssh2_exec($sconnection, $command);


ssh2_disconnect($sconnection);

?>
