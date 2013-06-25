<?php

function select_catagories() {
    // Allows the admin to select specific catagories
}

function random_select_catagories() {
    global $totalCatagories;
    $catagories = array();
    $required = $totalCatagories;
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
    // Reset all the catagories to non-active just in case
    $query = "UPDATE catagories SET active = 0";
    mysql_query ($query);

    // Reset all the questions
    $query = "UPDATE answers SET state = 0 WHERE state = 1";
    mysql_query ($query);

    // Set Catagory "active" to 1
    $query = "UPDATE catagories SET active = 1, used = 1, next = 0 WHERE cat_id = " . $cat_id;
    mysql_query ($query);

    // Pick the first question
    $query = "UPDATE answers SET state = 1 WHERE cat_id = " . $cat_id . " ORDER BY RAND() LIMIT 1";
    mysql_query ($query);

    // Show the penny
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
