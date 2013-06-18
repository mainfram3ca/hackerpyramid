#!/bin/bash

USER=`grep '$dbuser=' config.php | cut -d\" -f 2`
DB=`grep '$db=' config.php | cut -d\" -f 2`
PASS=`grep '$dbpass=' config.php | cut -d\" -f 2`

echo $USER
echo $DB
echo $PASS

mysqldump -u $USER -p$PASS $DB > dump.sql