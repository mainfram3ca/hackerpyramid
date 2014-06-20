<?php

include ('../base.php');

$query = "UPDATE  answers SET state =  '0'";
mysql_query($query);
$query = "UPDATE catagories SET used='0', next='0'";
mysql_query($query);
$query = "UPDATE teams SET enabled='1', score='0'";
mysql_query($query);


end_round();
