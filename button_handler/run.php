#!/bin/bash
<?php
## Run from Command Prompt

## TODO: BUG: What happens if all 3 judges buzz/accept?

while (true) {
    // Wait for a button to be pressed
    switch ($button) {
	case 'P':
	case 'p':
	    // A pass was requested
	    // Mark current as passed
	    // Select a new answer
	    break;
	case '1':
	case '2':
	case '3':
	    // A correct answer was given
	    // Select current answer
	    // See if a correct answer was already triggered
	    // If so, mark answer as correct
	    // If not, mark as answer accepted in variable
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
	    break;
    }
}
