'''
Synctify - Keep two directories in sync with the rsync utility.
'''

import config
import logger
import subprocess

my_config = config.config


def build_command():
    command = '''
    if [[ ! -d /Volumes/backup ]] ; then
        printf "Backup drive is not available. Exiting.\n"
        exit 1
    fi

    printf "Starting backup, please be patient.\n"

    rsync -av --delete -exclude=jeff/.Trash --exclude="Library" \
        /Users/jeff/ /Volumes/backup/jobs/ | tee ~/local/log/backup_momac.log
    rc=$?

    if [[ $rc -eq 0 ]] ; then
        printf "Backup completed successfully.\n"
        exit 0
    else printf "Backup failed!\n"
        exit 1
    fi
    '''

    return command


def process_command(command):
    output = subprocess.check_output(
        command,
        shell=True,
        stderr=subprocess.STDOUT,
    )
    return output


def get_config():
    my_config.load('Synctify.yaml')
    return '/Volumes/backup/jobs'


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


def run_rsync(destination):
    rc = 0
    my_stdout = None
    my_stderr = None
    try:
        my_stdout = subprocess.check_output(
            f'rsync -av --delete -exclude=jeff/.Trash --exclude="Library"  \
            /Users/jeff/Devl {destination}',
            shell=True,
            stderr=subprocess.STDOUT
           )
    except subprocess.CalledProcessError as e:
        rc = 1
        my_stderr = f'\nThe rsync command recieved the following error - \
            {e.stdout}'
    return rc, my_stdout, my_stderr


def main():
    my_log = logger.Logger()
    my_log.start()
    print("Synctify is starting...")
    destination = get_config()
    #  Test that the destination for the output is available.
    rc, output = check_destination(destination)
    if rc:
        print(output)
        return
    #  Run the Unix rsync command.
    rc, my_stdout, my_stderr = run_rsync(destination)
    if not rc:
        for line in my_stdout:
            print(line)
    if rc:
        for line in my_stderr.split("\n"):
            print(line)

    my_log.stop()


if __name__ == "__main__":
    main()
