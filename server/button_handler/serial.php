#!/usr/bin/env php
<?php
## Run from Command Prompt

## TODO: BUG: What happens if all 3 judges buzz/accept?

include "../base.php";
include "php_serial.class.php";

$minjudges = 2;

// Some variables to start
$quit = false;
$delaytime = 0;

function secho ($text) {
    // Were using a screen, so we need to \n everything. 
    echo $text . "\n";
}

function microtime_float()
{
        list($usec, $sec) = explode(" ", microtime());
        return ((float)$usec + (float)$sec);
}

$serial = new phpSerial;
$serial->deviceSet("/dev/ttyUSB0");
$serial->confBaudRate(9600);
$serial->confParity("none");
$serial->confCharacterLength(8);
$serial->confStopBits(1);
$serial->confFlowControl("none");

$serial->deviceOpen();

while (!$quit) {
    // Wait for a button to be pressed

    $read = '';
    $button = "";

    while ($read == '')  {
	$read = $serial->readPort(1);
        if ($read != '') {
                $button = $read;
        }
    }

    secho ("T: " . $button);
    // TODO: Need to check we're actually in an active round
    // Lets ignore one button for 5 seconds just incase a third judge triggers
    if ($button == "m") $quit = true;

    if (time() - $delaytime <= 5 && $button != 'm') {
	secho ("ignoring a button");
	$delaytime = 0;
    } elseif (get_status() == 2) {
    switch ($button) {
    	case 'p':
	    $cat_id = get_active_catagory();
    	    // A pass was requested
	    // Mark current as passed
	    answer_answered(2);
	    // Pick a new word
	    pick_answer($cat_id);
	    // Set a timestamp to weed out the extra judges
	    $delaytime = time();
	    // Select a new answer
	    secho ("Passed question");
	    break;
	case '1':
	case '2':
	case '3':
	    $cat_id = get_active_catagory();
	    // A correct answer was given
	    // Set the judges button to triggered
	    $tracker['correct'][$button]=1;
	    // See if more then X buttons were pressed
	    if (strlen(implode("",$tracker['correct'])) >= $minjudges) {
		// If so, mark answer as correct
		secho ("Judges say yes");
		// Give the active team a point
		add_point();
		// set the current answer to state 4
		answer_answered(4);
		// Pick a new word
		pick_answer($cat_id);
		// Set a timestamp to weed out the extra judges
		$delaytime = time();
		// clear the tracking variable
		$tracker['correct'] = array();
		$tracker['buzzed'] = array();
	    }
	    secho ("Correct Answer");
	    break;
	case 'q':
	case 'w':
	case 'e':
	    // A buzz was identified
	    // Set the judges button to triggered
	    $tracker['buzzed'][$button]=1;
	    // See if more then X buttons were pressed
	    if (strlen(implode("",$tracker['buzzed'])) >= $minjudges) {
		// If so, mark answer as correct
		secho ("Judges say NO");
		// set the current answer to state 4
		answer_answered(3);
		// Pick a new word
		pick_answer($cat_id);
		// Set a timestamp to weed out the extra judges
		$delaytime = time();
		// clear the tracking variable
		$tracker['correct'] = array();
		$tracker['buzzed'] = array();
	    }
	    secho ("Buzzed answer");
	    break;
    }
    }
}

$serial->deviceClose();
