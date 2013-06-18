<?php

include "config.php";

$mysql_link = mysql_connect('localhost', $dbuser, $dbpass);
mysql_select_db($db);
