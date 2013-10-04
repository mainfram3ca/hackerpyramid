#!/bin/bash

USER=`grep '$dbuser=' ../config.php | cut -d\" -f 2`
DB=`grep '$db=' ../config.php | cut -d\" -f 2`
PASS=`grep '$dbpass=' ../config.php | cut -d\" -f 2`

mysql -u $USER -p$PASS $DB < dump.sql