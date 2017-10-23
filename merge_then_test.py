"""
Merge same ending name files under same dir into one.
"""
import shutil
import os
import subprocess
import sys

class MissingFile(Exception):
    pass

def merge_files_to_one(file_paths, output_path):
    for a_path in file_paths:
        if not os.path.exists(a_path):
            raise MissingFile
    if os.path.exists(output_path):
        os.remove(output_path)
    # stackoverflow.com/a/27077437/1373296
    with open(output_path, 'a') as to_file:
        for a_path in file_paths:
            with open(a_path, 'r') as from_file:
                shutil.copyfileobj(from_file, to_file)
                to_file.write('\n\n')

def validate_file_path(a_path, target_ext, do_sth, target_filter=None):
    ext_len = len(target_ext)
    if os.path.isfile(a_path):
        a_name = os.path.basename(a_path)
        path_split = os.path.splitext(a_path)
        if path_split[1]:
            if target_filter is not None:
                if target_filter(a_name):
                    do_sth(a_path)
            else:
                do_sth(a_path)

def merge_files(file_paths, target_ext, save_under_path, file_name, merge_target_checker=None):
    paths_in = []
    def do_sth(a_path):
        paths_in.append(a_path)
    for a_path in file_paths:
        validate_file_path(a_path, target_ext, do_sth, merge_target_checker)
    path_out = os.path.join(save_under_path, file_name)
    merge_files_to_one(paths_in, path_out)

def source_paths_to_merge(under_path, target_ext, merge_target_checker=None):
    file_names = os.listdir(under_path)
    paths_to_merge = []
    ext_len = len(target_ext)
    for a_name in file_names:
        if len(a_name) >= ext_len:
            if a_name[-ext_len:] == target_ext:
                if merge_target_checker is not None:
                    if merge_target_checker(a_name):
                        paths_to_merge.append(os.path.join(under_path, a_name))
                else:
                    paths_to_merge.append(os.path.join(under_path, a_name))
    return paths_to_merge

def merge_files_under(under_path, target_ext, save_under_path, file_name, merge_target_checker=None):
    paths_in = source_paths_to_merge(under_path, target_ext, merge_target_checker)
    path_out = os.path.join(save_under_path, file_name)
    merge_files_to_one(paths_in, path_out)

"""
Assuming the folder to run test having two folders: src for source code and
tests for tests code. The merged file stored in
sub_path_of_exported_test_file (such as ./tests/runnable, inputed as
'tests/runnable') folder.
"""

passed_in_folder_path = "$folder_path"

def prepare_for_testing(ext_name, sub_path_of_exported_test_file='', test_file_name_mark=''):
    dir_path_out = os.path.join(passed_in_folder_path, sub_path_of_exported_test_file)
    if not os.path.exists(dir_path_out):
        os.makedirs(dir_path_out)
    src_paths = source_paths_to_merge(os.path.join(passed_in_folder_path, 'src'), ext_name)
    tests_paths = source_paths_to_merge(os.path.join(passed_in_folder_path, 'tests'), ext_name)
    file_name = ''.join(('to_run', test_file_name_mark, ext_name))
    merge_files_to_one(src_paths + tests_paths, os.path.join(dir_path_out, file_name))

def output_to_stdout(test_command, sub_path_of_exported_test_file=''):
    sys.stdout.write(os.path.join(passed_in_folder_path, sub_path_of_exported_test_file))
    sys.stdout.write('.')
    sys.stdout.write(test_command)
    sys.stdout.flush()
    sys.exit(0)

def run_py_tests():
    sub_path_runnable_test_file = 'env/bin/runnable_tests'
    prepare_for_testing('.py', sub_path_runnable_test_file, '_test')
    output_to_stdout('pytest', sub_path_runnable_test_file)

def run_js_tests():
    prepare_for_testing('.js')

file_ext_supported = {
    '.js': run_js_tests,
    '.py': run_py_tests,
}

def identify_src_ext(src_path):
    for a_name in os.listdir(src_path):
        a_path = os.path.join(src_path, a_name)
        if os.path.isfile(a_path):
            ext = os.path.splitext(a_path)[1]
            file_ext_supported[ext]()
            break

identify_src_ext(os.path.join(passed_in_folder_path, 'src'))
