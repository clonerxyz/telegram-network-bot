<?php
$output= shell_exec('sh ping.sh');
$a = json_encode($output);
header("Content-type:application/json");
echo str_replace("\\n", " ", $a)
?>
