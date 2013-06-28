<?php

    include "../base.php";

    // Select($from, $where='', $orderBy='', $limit='', $like=false, $operand='AND',$cols='*'

    // View -- The current view the end point should show
    // Values
    // 0 = Penny, Default Image
    // 1 = Catagories, The listing of available catagories
    // 2 = Word, The current word
    $out['view'] = 0;

    // Score -- The current Scores
    $out['score'] = 0;

    // Catagory -- 
    // If view = 1 - Array of Catagories
    // If view = 2 - The current catagory
    // $out['catagory'] = "Test";

    // Word -- The current word
    // $out['word'] = "word";

    $r_view = mysql_query("SELECT status FROM status WHERE type LIKE 'endpoint'");
    $out['view'] = intval(mysql_result($r_view,0));

    if ($out['view'] == 1) {
	// Get available catagories
	$out['catagory'] = array();
	$c_view = mysql_query("SELECT name, hint FROM catagories WHERE next = 1");
	while ($row = mysql_fetch_array($c_view, MYSQL_ASSOC)) {
	    array_push($out['catagory'], $row);
	}
    } elseif ($out['view'] == 2) {
	$c_view = mysql_query("SELECT c.name, c.hint, c.active, a.answer FROM catagories AS c, answers AS a WHERE c.active > 0 AND a.state = 1 and c.cat_id = a.cat_id LIMIT 1");
	$row = mysql_fetch_array($c_view, MYSQL_ASSOC);
	$out['catagory'] = $row['name'];
	$out['word'] = $row['answer'];
	// Get current word
	$query = "SELECT status FROM status WHERE type LIKE 'timer'";                                                
	$result = mysql_query($query);                                                                               
	$time = mysql_result($result,0);                                                                             
	// Show the timer:                                                                                           
	$out['time'] = $time + $TOTALTIME - time();                                                                 
    }

    echo json_encode($out);
