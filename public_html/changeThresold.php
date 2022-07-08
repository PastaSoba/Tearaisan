<?php
define("ADDRESS","127.0.0.1");
define("USER","pi");
define("PASSWORD","raspberry");
 
If(!is_null($_GET["value"])){

/* SSH2 module processes */
$sconnection = ssh2_connect(ADDRESS,22);
ssh2_auth_password($sconnection,USER,PASSWORD);


//ファイル読む
$MCjson = file_get_contents("/home/pi/system_pid.log");
echo $MCjson;
// echo "aaa";
 
 
//kill
$command = "/usr/bin/sudo /usr/bin/kill ".$MCjson;
ssh2_exec($sconnection,$command);
 
 
// 閾値変更
$command = "/usr/bin/sudo /usr/bin/python3 /home/pi/codes/main.py ".$_GET["value"]." &";
$stdio_stream = ssh2_exec($sconnection,$command);
ssh2_disconnect($sconnection);
// echo("result: $contents");

}
?>
