import logging as log
from subprocess import Popen, PIPE


#  r u n _ s h e l l _ c m d s
#  Standard function for consistent method to run shell commands
def run_shell_cmds(cmds):
    log.info(f'begin run_shell_cmds({cmds})')
    process = Popen(
        cmds,
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )
#         universal_newlines=True,

    try:
        stdout, stderr = process.communicate()
    finally:
        rc = process.returncode
    log.info(f'end   run_shell_cmds - returns {rc}')
    return rc, stdout, stderr
