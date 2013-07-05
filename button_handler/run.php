#!/usr/local/bin/php
<?php
## Run from Command Prompt

## TODO: BUG: What happens if all 3 judges buzz/accept?

include "../base.php";

$minjudges = 2;

// Some variables to start
$quit = false;
$delaytime = 0;

function getch() {
    // Not sure if ncurses works yet, so let's leave it out.
//    if (function_exists('ncurses_getch')) {
//	return ncurses_getch();
//    } else {
	$term = `stty -g`;
	// Make lots of drastic changes to the tty
	system("stty raw opost -ocrnl onlcr -onocr -onlret icrnl -inlcr -echo isig intr undef");
	$buf = fread(STDIN, 1);
	system("stty " . $term);
	return $buf;
//    }
}

function secho ($text) {
    // Were using a screen, so we need to \n everything. 
    echo $text . "\n";
}

while (!$quit) {
    // Wait for a button to be pressed
    $button = strtolower(getch());
    secho ($button);
    // Lets ignore one button for 5 seconds just incase a third judge triggers
    if (time() - $delaytime <= 5 && $button != 'm') {
	secho ("ignoring a button");
	$delaytime = 0;
    } else {
    switch ($button) {
    	case 'p':
    	    // A pass was requested
	    // Mark current as passed
	    // Select a new answer
	    secho ("Passed question");
	    break;
	case '1':
	case '2':
	case '3':
	    // A correct answer was given
	    // Select current answer
	    // Set the judges button to triggered
	    $tracker['correct'][$button]=1;
	    // See if more then X buttons were pressed
	    if (strlen(implode("",$tracker['correct'])) >= $minjudges) {
		// If so, mark answer as correct
		secho ("Judges say yes");
		// Set a timestamp to weed out the extra judges
		$delaytime = time();
		// clear the variable
		$tracker['correct'] = array();
	    }
	    secho ("Correct Answer");
	    break;
	case 'q':
	case 'w':
	case 'e':
	    // A buzz was identified
	    // Select current answer
	    // See if a buzzed answer was already triggered
	    // If so, mark answer as buzzed
	    // If not, mark as answer buzzed in variable
	    secho ("Buzzed answer");
	    break;
	case 'm':
	    $quit = true;
	    break;
    }
    }
}

