#!/usr/local/bin/php
<?php
## Run from Command Prompt

## TODO: BUG: What happens if all 3 judges buzz/accept?

include "../base.php";

$term = `stty -g`;
$quit = false;

// Make lots of drastic changes to the tty
system("stty raw opost -ocrnl onlcr -onocr -onlret icrnl -inlcr -echo isig intr undef");

function getch() {
    if (function_exists('ncurses_getch')) {
	return ncurses_getch();
    } else {
	$buf = fread(STDIN, 1);
	return $buf;
    }
}

function secho ($text) {
    echo $text . "\n";
}

while (!$quit) {
    // Wait for a button to be pressed
    $button = getch();
    secho ($button);
    switch ($button) {
	case 'P':
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
	    // See if a correct answer was already triggered
	    // If so, mark answer as correct
	    // If not, mark as answer accepted in variable
	    secho ("Correct Answer");
	    break;
	case 'q':
	case 'Q':
	case 'w':
	case 'W':
	case 'e':
	case 'E':
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

system("stty " . $term);
