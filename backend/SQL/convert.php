<?php

include ('base.php');

$query = "SELECT cat_id, answers FROM catagories";

$result = mysql_query($query);                                                                               
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {                                                     
    $answers = explode(",", $row['answers']);
    foreach ($answers as $answer) {
	if ($answer != "") {
	    $query2 = "INSERT INTO answers (cat_id, answer) VALUES (". $row['cat_id']  .", '" . $answer . "');";
	    mysql_query($query2);
	}
    }
}  