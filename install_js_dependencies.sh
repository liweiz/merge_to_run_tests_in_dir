#!/bin/bash

# command not found via shell script but works on terminal: unix.stackexchange.com/questions/163120/command-not-found-via-shell-script-but-works-on-terminal

PATH=$PATH:/bin:/usr/local/bin:yarn
export PATH

# This is after the the source code foler copied to the folder to do test. The
# last action's returned path is the first element of the list.
# Assuming this script is called right after the copy action, $1 would be the
# path of the destination folder.

folder_path_to_do_test="${1}"
echo "$folder_path_to_do_test"

cd $folder_path_to_do_test

yarn
