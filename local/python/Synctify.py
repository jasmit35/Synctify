'''
Synctify - Keep two directories in sync with the rsync utility.
'''

import argparse
import config
import logging as log
from pathlib import Path
import sys

from run_shell_cmds import run_shell_cmds
from gmailer import Gmailer

env_specific_params = None


def my_startup():
    global env_specific_params

    comandline_arguments = get_cmdline_args()
    cfgfile = comandline_arguments.cfgfile
    environment = comandline_arguments.environment

    cfgfile_params = config.Config(f'../etc/{cfgfile}')
    env_specific_params = cfgfile_params[f'{environment}']

    log_level = env_specific_params['log_level']

    if log_level == 'DEBUG':
        log_level = log.DEBUG
    else:
        if log_level == 'INFO':
            log_level = log.INFO

    log.basicConfig(level=log_level,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[log.FileHandler(filename='../log/synctify.log')]
                    )


def get_cmdline_args():
    parser = argparse.ArgumentParser(description="Synctify")
    parser.add_argument(
        "-e", "--environment",
        required=True,
        choices=["devl", "test", "prod"],
        help="Environment - devl, test or prod"
    )
    parser.add_argument(
        "-c", "--cfgfile",
        required=False,
        default="synctify.cfg",
        help="Name of the configuration file to use"
    )
    args = parser.parse_args()
    return args


def my_shutdown(rc=0, sysout=None, syserr=None):

    gmail_cfg_file = env_specific_params['jeff_home'] + "/.gmail.yaml"
    gmail_params = config.Config(gmail_cfg_file)
    gword = gmail_params['Gmailer.password']

    mailer = Gmailer(gword)
    log.info("Sending log file...")
    log.shutdown()

    message = "Subject: Synctify logs\n"

    message += "\nStart of .out file...\n"
    sys.stdout.flush()
    with open("../log/synctify.out", 'r') as f:
        message += f.read()

    message += "\nStart of .err file...\n"
    with open("../log/synctify.err", 'r') as f:
        message += f.read()

    if rc not in [0, 23]:
        message += "\nStart of .log file...\n"
        with open("../log/synctify.log", 'r') as f:
            message += f.read()

    message += "\nend of message\n"

    mailer.send("js8335@swbell.net", message)

    sys.exit(rc)


def build_command_string(source, destination):
    command = f'''rsync -av --no-perms --delete \
        --exclude=jeff/.Trash \
        --exclude="Library" \
        "{source}" \
        "{destination}"
    '''
    return command


def main():
    my_startup()
    log.info("begin main()")

    source = env_specific_params['source_dir']
    destination = env_specific_params['destination_dir']

    test_path = Path(destination)
    if Path.exists(test_path) is False:
        print(f"The destination path \"{destination}\" does not exist. Terminating.")
        my_shutdown(128)

    cmd = build_command_string(source, destination)

    rc, stdout, stderr = run_shell_cmds(cmd)
    sys.stdout.buffer.write(stdout)
    if not rc:
        sys.stderr.buffer.write(stderr)

    my_shutdown(rc, stdout, stderr)


if __name__ == "__main__":
    main()
