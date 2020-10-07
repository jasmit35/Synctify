#!/usr/bin/env python3
"""
auto_update.py
"""
import argparse
import os
import pathlib
import shutil
import subprocess
import sys

# import modules.DBSecEnvironment as dbse

auto_update_version = "4.2.5"


def get_config():

    parser = argparse.ArgumentParser(description="auto_update")
    parser.add_argument(
        "-e", "--environment", required=True,
        help="Environment (devl, test, prod"
    )
    args = parser.parse_args()
    environment = args.environment
    return environment


#  Standard function for consistent method to run shell commands
def run_shell_cmds(cmds):

    process = subprocess.Popen(
        "/bin/bash",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    try:
        out, err = process.communicate(cmds)
        rc = process.returncode
    except Exception as e:
        print(f"Exception occured {e}")
        rc = process.returncode

    return rc, out, err


#  Copy the files we want
def copy_files(source_dir, source_files, target_dir, files_mode):

    #  Test that the directories exists
    if not pathlib.Path(source_dir).is_dir():
        print('The source directory "{}" does not exist!'.format(source_dir))
        return 1

    if not pathlib.Path(target_dir).is_dir():
        print('The target directory "{}" does not exist!'.format(target_dir))
        return 1

    #  Try the copies
    for file in source_files:

        source_file = source_dir + "/" + file
        target_file = target_dir + "/" + file

        print('    Updating file "{}"\n'.format(target_file))

        try:
            shutil.copyfile(source_file, target_file)
        except FileNotFoundError:
            print(f"    The file {source_file} was not in the source.\n")
            continue

        os.chmod(target_file, files_mode)


def main():
    env_num = 0
    while env_num not in ["1", "2", "3"]:
        print("Select environment - ( 1 = devl, 2 = test, 3 = prod) ===> ")
        env_num = input()

    if env_num == "1":
        environment = 'Devl'
    elif env_num == "2":
        environment = 'Test'
    elif env_num == "3":
        environment = 'Prod'
    else:
        print("Please enter 1, 2 or 3")

    APP_NAME = "Synctify"
    APP_HOME = "/Users/Jeff/" + environment + "/" + APP_NAME

    required_dirs = []
    required_dirs.append(APP_HOME)

    required_dirs.append(APP_HOME + "/local")
    required_dirs.append(APP_HOME + "/local/python")
    required_dirs.append(APP_HOME + "/local/bin")
    required_dirs.append(APP_HOME + "/local/log")
    required_dirs.append(APP_HOME + "/local/cron")

    for dir in required_dirs:
        if not pathlib.Path(dir).is_dir():
            print("Error! Required directory {} does not exist.".format(dir))
            sys.exit(1)

    #
    #  Primary python programs
    source_files = [
        "Synctify.py",
        "config.py",
        "gmailer.py",
        "logger.py",
        "run_shell_cmds.py"
    ]
    tmp_dir = "/tmp"
    source_dir = tmp_dir + "/" + APP_NAME + "/src/Synctify/core"
    target_dir = APP_HOME + "/local/python"
    copy_files(source_dir, source_files, target_dir, 0o750)

    #  Shell script used to run Python scripts with the right Python version
    source_files = [
        "runmypy.sh"
    ]
    source_dir = tmp_dir + "/" + APP_NAME + "/src/Synctify/core"
    target_dir = APP_HOME + "/local/bin"
    copy_files(source_dir, source_files, target_dir, 0o750)

    #  Configuration files
    source_files = [
        "requirements.txt",
        "Synctify.yaml"
    ]
    source_dir = tmp_dir + "/" + APP_NAME
    target_dir = APP_HOME + "/local/python"
    copy_files(source_dir, source_files, target_dir, 0o750)


    return
    #
    #  Python modules used by the main Python scripts.
    source_files = [
        "DBSecEnvironment.py",
        "asprloggingchk.py",
        "asprloginchk.py",
        "asprpasswdchk.py",
        "asprversionchk.py",
        "dbsec_sql.py",
        "jspgeng.py",
        "jsstdrpt.py",
        "process_uam.py",
        "report1.py",
        "report2.py",
        "report3.py",
        "tab_allusers.py",
        "tab_databases.py",
        "tab_invalidusers.py",
        "tab_nodes.py",
        "tab_regions.py",
        "tab_validusers.py",
    ]
    source_dir = tmp_dir + "/dbsec/local/python/modules"
    target_dir = dbsec_home + "/local/python/modules"
    copy_files(source_dir, source_files, target_dir, 0o750)
    #
    #  Python used for reporting.
    source_files = [
        "ASPRaudit.py",
        "StdReports.py",
        "UserAudit.py",
    ]
    source_dir = tmp_dir + "/dbsec/local/python/reports"
    target_dir = dbsec_home + "/local/python/reports"
    copy_files(source_dir, source_files, target_dir, 0o750)

    source_dir = tmp_dir + "/dbsec/local/bin"
    target_dir = dbsec_home + "/local/bin"
    copy_files(source_dir, source_files, target_dir, 0o750)
    #
    #  SQL files for tables, views and roles.
    source_files = [
        "aic30_nodes_view.sql",
        "allusers.sql",
        "components.sql",
        "compusers.sql",
        "databases.sql",
        "dbtypes.sql",
        "dbversions.sql",
        "installations.sql",
        "invalidusers.sql",
        "invalidusers_vw.sql",
        "jumpservers.sql",
        "nodecomps.sql",
        "nodes.sql",
        "platforms.sql",
        "regions.sql",
        "reset_all.sql",
        "reset_postgres.sql",
        "validusers.sql",
        "validusers_vw.sql",
    ]
    source_dir = tmp_dir + "/dbsec/local/sql"
    target_dir = dbsec_home + "/local/sql"
    copy_files(source_dir, source_files, target_dir, 0o750)
    #
    #  SQL files to handle data transfer for version 4 upgrade
    source_files = [
        "load_allusers.sql",
        "load_compusers.sql"
    ]
    copy_files(source_dir, source_files, target_dir, 0o750)

    #
    #  Cleanup
    shutil.rmtree(tmp_dir + "/dbsec")

    print("Success!")

    sys.exit(0)


if __name__ == "__main__":
    main()
