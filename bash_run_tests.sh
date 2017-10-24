#!bin/bash

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
a_dir_path="$(dir_path "$passed_from_stdout")"

echo $1
echo $command_text
echo $a_dir_path

cd "$a_dir_path"

export working_path="$a_dir_path"

cat << EOF > run_tests_now.sh
#!/bin/bash
cd "$working_path"
source ../env/bin/activate
python -m $command_text

EOF

chmod 755 run_tests_now.sh

open -a terminal.app run_tests_now.sh
