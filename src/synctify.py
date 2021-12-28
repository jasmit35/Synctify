'''
Synctify - Keep two directories in sync with the rsync utility.
'''

from __init__ import __version__
from argparse import ArgumentParser
import config
import os
from pathlib import Path
from re import sub
import sys
from traceback import print_exc

from run_shell_cmds import run_shell_cmds
from gmailer import Gmailer


shared_code_path = os.path.abspath("../local/python")
sys.path.insert(1, shared_code_path)
from base_app import BaseApp


#  =============================================================================
class Synctify(BaseApp):

    def __init__(self, app_name, version):
        super().__init__(app_name, version)

    #  -----------------------------------------------------------------------------
    def set_cmdline_params(self):
        parser = ArgumentParser(description="TRORpts")
        parser.add_argument(
            "-e", "--environment", required=True, help="Environment - devl, test or prod"
        )
        parser.add_argument(
            "-c", "--cfgfile", required=False, help='Configuration file name'
        )
        args = parser.parse_args()
        return vars(args)

    #  -----------------------------------------------------------------------------
    def process(self):
        self.info('begin process()')

        source, destination = self.verify_directories()

        cmd = self.build_command_string(source, destination)

        rc, my_stdout, my_stderr = run_shell_cmds(cmd)
        sys.stdout.buffer.write(my_stdout)
        sys.stderr.buffer.write(my_stderr)

        # self.email_results(this_app, rc)
        message = self.build_message(rc)

        self.email_message(message)

        self.info(f"end   process - returns {rc=}")
        return rc

    #  -----------------------------------------------------------------------------
    def verify_directories(self):
        self.info('begin verify_directories()')
        source = self.cfgfile_params.get('source_dir', None)
        destination = self.cfgfile_params.get('destination_dir', None)

        for test_path_str in source, destination:
            self.output(f"The directory'{test_path_str}' ")
            test_path = Path(test_path_str)
            if Path.exists(test_path):
                self.output("is valid.\n")
            else:
                self.output("does not exist! Terminating.")
                this_app.destruct(self, 128)

        self.info(f'end   verify_directories - returns {source=}. {destination=}')
        return source, destination

    #  -----------------------------------------------------------------------------
    def build_command_string(self, source, destination):
        self.info(f"begin build_command_string({source=}, {destination=})")

        command = 'rsync -avo --no-perms --delete --ignore-errors '

        excludes = this_app.cfgfile_params.get('excludes')
        for excl in excludes:
            command += f" {excl} "

        command += f"'{source}' '{destination}'"
        command = sub(" +", " ", command)

        self.output(f"Using the following command:\n{command}\n")
        self.info(f"end   build_command_sring - returns {command=}")
        return command

    #  -----------------------------------------------------------------------------
    def email_results(self, rc=0, sysout=None, syserr=None):
        # gmail_cfg_file = env_specific_params['jeff_home'] + "/.gmail.yaml"
        gmail_cfg_file = this_app.cfgfile_params.get('jeff_home') + "/.gmail.yaml"
        gmail_params = config.Config(gmail_cfg_file)
        gword = gmail_params['Gmailer.password']

        mailer = Gmailer(gword)
        this_app.info("Sending log file...")

        message = "Subject: Synctify logs\n"

        message += "\nStart of .out file...\n"
        sys.stdout.flush()
        with open("./local/log/synctify.out", 'r', encoding='utf-8') as f:
            message += f.read()

        message += "\nStart of .err file...\n"
        with open("./local/log/synctify.err", 'r') as f:
            message += f.read()

        if rc not in [0, 23]:
            message += "\nStart of .log file...\n"
            with open("./local/log/synctify.log", 'r') as f:
                message += f.read()

        message += "\nend of message\n"

        mailer.send("js8335@swbell.net", message)

    #  -----------------------------------------------------------------------------
    def build_message(self, rc):
        self.info(f"begin build_message({rc=})")

        message = "Subject: Synctify report\n"
        if rc == 0:
            message += self.output_report.get_contents()

            sys.stdout.flush()
            with open("./local/log/synctify.out", 'r', encoding='utf-8') as f:
                message += f.read()

        else:
            message += "\nStart of .out file...\n"

            sys.stdout.flush()
            with open("./local/log/synctify.out", 'r', encoding='utf-8') as f:
                message += f.read()

            message += "\nStart of .err file...\n"
            with open("./local/log/synctify.err", 'r') as f:
                message += f.read()

            if rc not in [0, 23]:
                message += "\nStart of .log file...\n"
                with open("./local/log/synctify.log", 'r') as f:
                    message += f.read()

        message += "\nend of message\n"

        self.info("end   build_message - returns ...")
        return message

    #  -----------------------------------------------------------------------------
    def email_message(self, message):
        self.info('begin email_message(...)')

        gmail_cfg_file = self.cfgfile_params.get('jeff_home') + "/.gmail.yaml"
        gmail_params = config.Config(gmail_cfg_file)
        gword = gmail_params['Gmailer.password']
        mailer = Gmailer(gword)

        mailer.send("js8335@swbell.net", message)

        self.info('end   email_message - returns None')

    #  -----------------------------------------------------------------------------
    def destruct(self, rc):
        super().destruct(rc)


#  =============================================================================
if __name__ == "__main__":
    try:
        this_app = Synctify('synctify', __version__)
        rc = this_app.process()
        this_app.destruct(rc)
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
