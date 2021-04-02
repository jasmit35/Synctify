'''
Synctify - Keep two directories in sync with the rsync utility.
'''

import config
import logging
# import subprocess 
import sys

from run_shell_cmds import run_shell_cmds
from gmailer import Gmailer


def my_begin():
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    logging.info("Synctify is starting...")


def std_end(rc=0, sysout=None, syserr=None, gword=None):

    mailer = Gmailer(gword)
    logging.info("Sending log file...")
    logging.shutdown()

    message = "Subject: Test message\n"

    message += "Start of log file...\n"

    sys.stdout.flush()

    with open("../log/Synctify.log", 'r') as f:
        message += f.read()

#     message += "Start of error file...\n"
#     with open("../log/Synctify.err", 'r') as f:
#         message += f.read()

    mailer.send("js8335@swbell.net", message)

    sys.exit(rc)


def std_end2(rc=0):

    cfg = config.Config('/Users/Jeff/.gmail.yaml')
    gword = cfg['Gmailer.password']
    mailer = Gmailer(gword)

    logging.info("Sending log file...")

    message = "Subject: Test message\n"

    message += "Start of log file...\n"

    sys.stdout.flush()
    sys.stderr.flush()

    with open("../log/Synctify.log", 'r') as f:
        message += f.read()

    mailer.send("js8335@swbell.net", message)

    sys.exit(rc)


def get_config():
    cfg = config.Config('/Users/Jeff/.gmail.yaml')
    gword = cfg['Gmailer.password']

    my_config = config.Config('Synctify.yaml')
    return '/Users/Jeff/devl', str("/System/Volumes/Data/Volumes/Backup\ Share/Jobs/Synctify/users/jeff"), gword


def check_destination(destination):
    logging.info(f'begin check_destination({destination})')
#     rc = 0
#     try:
#         output = subprocess.check_output(
#             f'test -d {destination}',
#             shell=True,
#             stderr=subprocess.STDOUT
#            )
#     except subprocess.CalledProcessError:
#         rc = 1
#         output = f'The destionation {destination} is not an existing directory'
#    std_end(rc, output, stderr, gword) 
    #  Run the command.
    cmd = f'test -d {destination}'
    rc, stdout, stderr = run_shell_cmds(cmd)
    logging.info(f'end  check_destination - returns {rc}, {stdout}, {stderr}')
    return rc, stdout, stderr


def build_command_string(source, destination):
    command = f'''rsync -at --delete \
        --exclude=jeff/.Trash \
        --exclude="Library" \
        {source} \
        {destination}
    '''
    return command


def main():
    my_begin()
    logging.info("begin main()")

    source, destination, gword = get_config()

    #  Test that the destination for the output is available.
    rc, stdout, stderr = check_destination(destination)
    if rc:
        std_end2(rc)

    #  Build the command string.
    cmd = build_command_string(source, destination)

    #  Run the command.
    rc, stdout, stderr = run_shell_cmds(cmd)
    sys.stdout.buffer.write(stdout)
    if not rc:
        sys.stderr.buffer.write(stderr)

    std_end(rc, stdout, stderr, gword)


if __name__ == "__main__":
    main()
