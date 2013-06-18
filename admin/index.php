<?php

include "../base.php";

$TOTALTIME=60;

function select_catagories() {
    // Allows the admin to select specific catagories
}

function random_select_catagories() {
    $catagories = array();
    $required = 5;
    // Select random catagories and ensure 6 are available
    // Find out how many catagories we need
    $query = "SELECT count(*) FROM catagories WHERE next = 1";
    $result = mysql_query($query);
    $have = mysql_result($result,0);

    if ($required <= $have) {
	echo "We have enough<BR><BR>";
	return;
    }

    // Get the list of available catagories
    $query = "SELECT cat_id FROM catagories WHERE next = 0 AND used = 0";
    $result = mysql_query($query);
    // Loop though and build a list of available catagories
    while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	array_push($catagories, $row['cat_id']);
    }
    // Pick the required extra catagories
    $selected = array_rand($catagories, $required - $have);
//    print_r($selected);
    if (is_array($selected)) {
	foreach ($selected as $item) {
	    $query = "UPDATE catagories SET next = 1 WHERE cat_id = " . $catagories[$item];
//	    echo $catagories[$item] . "<br>";
	    mysql_query ($query);
	}
    } else {
	$query = "UPDATE catagories SET next = 1 WHERE cat_id = " . $catagories[$selected];
	mysql_query ($query);
    }    
}

function set_catagory($cat_id) {
    // Set the active catagory
    // Set Catagory "active" to 1
    $query = "UPDATE catagories SET active = 0";
    mysql_query ($query);
    $query = "UPDATE catagories SET active = 1, used = 1, next = 0 WHERE cat_id = " . $cat_id;
    mysql_query ($query);
    $query = "UPDATE status SET status = 0 WHERE type LIKE 'endpoint'";
    mysql_query ($query);
}

function reset_catagories() {
    // Reset between groups of people, leave used ones used
    $query = "UPDATE catagories SET active = 0, next = 0";
    mysql_query ($query);
}

function start_round() {
    // start the round
    // Set Endpoint status to 2
    $query = "UPDATE status SET status = 2 WHERE type LIKE 'endpoint'";
    mysql_query ($query);
    // Start clock
    $query = "UPDATE status SET status = " . time() . " WHERE type LIKE 'timer'";
    mysql_query ($query);
}

function show_catagories() {
    // start the round
    // Set Endpoint status to 3
    $query = "UPDATE status SET status = 1 WHERE type LIKE 'endpoint'";
    mysql_query ($query);
}


function end_round() {
    $query = "UPDATE catagories SET active = 0";
    mysql_query ($query);
    $query = "UPDATE status SET status = 0 WHERE type LIKE 'endpoint'";
    mysql_query ($query);
}

function show_penny() {
    $query = "UPDATE status SET status = 0 WHERE type LIKE 'endpoint'";
    mysql_query ($query);
}

switch ($_GET['command']) {
    case "rsc":
	random_select_catagories();
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
<a href="?command=penny">Show Penny</a><BR>
<a href="?command=rsc">Random Select Catagory</a><BR>
<a href="?command=show">Show Catagories</a><BR>
<a href="?command=start">Start Rount</a><BR>
<a href="?command=stop">Stop Round</a><BR>
<a href="?command=refresh">Refresh</a><BR>
<BR><BR><BR>
<a href="?command=reset">Reset Catagory</a><BR>

<?php
$query = "SELECT status FROM status WHERE type LIKE 'endpoint'";
$result = mysql_query($query);
if (mysql_result($result,0) == 2) {

?>
<BR>
Time Left: <div id="timer"></div>

<script>
    function loadXMLDoc()
    {
	var xmlhttp;
	if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
	    xmlhttp=new XMLHttpRequest();
	} else {// code for IE6, IE5
	     xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function() {
	    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
		data = JSON.parse(xmlhttp.responseText);
		document.getElementById("timer").innerHTML=data.left
	    }
	}
	xmlhttp.open("GET","ajax_info.php",true);
	xmlhttp.send();
    }

    setInterval(loadXMLDoc, 1000);
</script>

<?php 
}