'''
Synctify - Keep two directories in sync with the rsync utility.
'''

import config
import logger
import subprocess
import sys

from run_shell_cmds import run_shell_cmds
from gmail import Gmailer

my_config = config.config
my_log = None


def std_begin():
    global my_log
    my_log = logger.Logger()
    my_log.start()
    my_log.info("Synctify is starting...")


def std_end(rc=0, sysout=None, syserr=None):
    global my_log
    my_log.stop()

    mailer = Gmailer("password")
    mailer.send("js8335@swbell.net", my_log)


def get_config():
    my_config.load('Synctify.yaml')
    return '/Users/Jeff', '/System/Volumes/Data/Volumes/backup/jobs'


def check_destination(destination):
    rc = 0
    try:
        output = subprocess.check_output(
            f'test -d {destination}',
            shell=True,
            stderr=subprocess.STDOUT
           )
    except subprocess.CalledProcessError:
        rc = 1
        output = f'The destionation {destination} is not an existing directory'
    return rc, output


def build_command_string(source, destination):
    command = f'''rsync -av --delete \
        --exclude=jeff/.Trash \
        --exclude="Library" \
        {source} \
        {destination}
    '''
    return command


def main():
    std_begin()
    source, destination = get_config()
    #  Test that the destination for the output is available.
    rc, output = check_destination(destination)
    if rc:
        print(output)
        return

    #  Build the command string.
    cmd = build_command_string(source, destination)

    #  Run the command.
    rc, stdout, stderr = run_shell_cmds(cmd)
    sys.stdout.buffer.write(stdout)
    if not rc:
        sys.stderr.buffer.write(stderr)

    std_end()


if __name__ == "__main__":
    main()
