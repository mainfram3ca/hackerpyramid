<?php

include "../base.php";

switch ($_GET['command']) {
    case "rsc":
	random_select_catagories();
	break;
    case "videos":
 	show_videos();
	break;
    case "penny":
 	show_penny();
	break;
    case "reset":
	reset_catagories();
	break;
    case "show":
	show_catagories();
	break;
    case "set":
	// validate it's a number first stupid
	if (is_numeric($_GET['id'])) { 
	    set_catagory($_GET['id']);
	} else {
	    echo "WHAT ARE YOU DOING?";
	}
	break;
    case "start":
 	start_round();
	break;
    case "stop":
	end_round();
	break;
}

// List the active catagories so we can select them. 
$query = "SELECT cat_id, name FROM catagories WHERE next = 1";
$result = mysql_query($query);
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
    echo "<A href='?command=set&id=" . $row['cat_id'] . "'>" . $row['name'] . "</a><BR>";
}

?>
<BR><BR><BR>
<a href="?command=videos">Show Videos</a><BR>
<a href="?command=penny">Show Penny</a><BR>
<a href="?command=rsc">Random Select Catagory</a><BR>
<a href="?command=show">Show Catagories</a><BR>
<a href="?command=start">Start Round</a><BR>
<a href="?command=stop">Stop Round</a><BR>
<a href="?command=refresh">Refresh</a><BR>
<BR><BR><BR>
<a href="?command=reset">Reset Catagory</a><BR>

<?php
// Show the timer if we're in round
$query = "SELECT status FROM status WHERE type LIKE 'endpoint'";
$result = mysql_query($query);
if (mysql_result($result,0) == 2) {

?>
<BR>
Time Left: <div id="timer"></div>

<script src="../assets/jquery-2.0.2.min.js"></script>
<script src="json_handler.js"></script>

<?php 
}
