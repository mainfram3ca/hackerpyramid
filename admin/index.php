<?php

include "../base.php";

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
	echo "We have enough";
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
    if (is_array($selected)) {
	foreach ($selected as $item) {
	    $query = "UPDATE catagories SET next = 1 WHERE cat_id = " . $item;
	    mysql_query ($query);
	}
    } else {
	$query = "UPDATE catagories SET next = 1 WHERE cat_id = " . $selected;
	mysql_query ($query);
    }    
}

function reset_select_catagories() {
    // Reset the catagories between player sets
}

function set_catagory($cat_id) {
    // Set the active catagory
    // Set Catagory "active" to 1
    $query = "UPDATE catagories SET active = 1, used = 1, next = 0 WHERE cat_id = " . $cat_id;
    mysql_query ($query);
}

function start_round() {
    // start the round
    // Set Endpoint status to 2
    // Start clock
}

function end_round() {
    $query = "UPDATE catagories SET active = 0";
    mysql_query ($query);
}

function manage_reponse() {
    // Handle Skip option
}

random_select_catagories();
// set_catagory(13);
// end_round();
