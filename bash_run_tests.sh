#!bin/bash

# command not found via shell script but works on terminal: unix.stackexchange.com/questions/163120/command-not-found-via-shell-script-but-works-on-terminal

# Previous run script passes two arguments (path of selected folder and test 
# command to run in this new terminal) in form of path.command.
# e.g., /home/martin/docs.pytest means
# dir path: /home/martin/docs
# test command: pytest

passed_from_stdout=$1

function file_extension() {
    echo "${1##*.}"
}

function dir_path() {
    echo "${1%.*}"
}

command_text="$(file_extension "$passed_from_stdout")"
a_test_field_dir_path="$(dir_path "$passed_from_stdout")"

cd "$a_test_field_dir_path"

# This is the path of folder "runnable_tests" which is at the same level as src.
export working_path="$a_test_field_dir_path"
export test_file_abs_path="${a_test_field_dir_path}/to_run.js"

cat << EOF > run_tests_now.sh
#!/bin/bash
cd "$working_path"
if [ "$command_text" = "pytest" ]
then
    source ../env/bin/activate
    python -m $command_text
elif [ "$command_text" = "ava" ]
then
    PATH=$PATH:/bin:/usr/local/bin:yarn
    export PATH
    yarn test "$test_file_abs_path"
else
    echo '$command_text is' $command_text
fi

EOF

chmod 755 run_tests_now.sh

open -a terminal.app run_tests_now.sh
