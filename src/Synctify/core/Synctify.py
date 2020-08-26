#!/usr/bin/env python
'''
Synctify - Keep two directories in sync with the rsync utility.
'''

import config
import logger


my_config = config.config


def get_config():
    my_config.load('Synctify.yaml')
    return


def build_command():
    command = f'rsync {my_config}'
    return command


def process_command(command):
    print(f'The completed command was "{command}"')


def main():
    my_log = logger.Logger()
    my_log.start()
    print("Hello from the Synctify app!")
    get_config()
    command = build_command()
    process_command(command)
    my_log.stop()


if __name__ == "__main__":
    main()
