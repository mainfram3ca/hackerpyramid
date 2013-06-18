<?php

include "../base.php";

$query = "SELECT status FROM status WHERE type LIKE 'endpoint'";
$result = mysql_query($query);
$status = mysql_result($result,0);

if ($status == 2) {
    $query = "SELECT status FROM status WHERE type LIKE 'timer'";
    $result = mysql_query($query);
    $time = mysql_result($result,0);
    // Show the timer:
    $left['left'] = $time + $TOTALTIME - time();
    // Timer Functions
    if ($left['left'] <= 0) {
	// We're out of time
        $query = "UPDATE catagories SET active = 0";                                                                 
	mysql_query ($query);                                                                                        
        $query = "UPDATE status SET status = 0 WHERE type LIKE 'endpoint'";                                          
	mysql_query ($query); 
    }
} else {
    $left['left'] = 0;
}

echo json_encode($left);
