import sys
import traceback
from subprocess import STDOUT, CalledProcessError, check_output

from great_expectations.core import logger


def execute_shell_command(command: str, *, cwd: str = None, env: dict = None) -> int:
    # TODO[Alex] progress bar https://click.palletsprojects.com/en/7.x/utils/#showing-progress-bars
    # TODO[Alex] change loggers to more appropriate level
    logger.critical(f"\n\nrunning execute_shell_command for {command}")
    status_code: int = 0
    try:
        sh_out: str = check_output(
            ["bash", "-c", command],
            cwd=cwd,
            env=env,
            shell=False,
            stderr=STDOUT,
            universal_newlines=True,
        )
        sh_out = sh_out.strip()
        logger.critical(sh_out)
    except CalledProcessError as cpe:
        status_code = cpe.returncode
        sys.stderr.write(cpe.output)
        sys.stderr.flush()
        exception_message: str = "A Sub-Process call Exception occurred.\n"
        exception_traceback: str = traceback.format_exc()
        exception_message += (
            f'{type(cpe).__name__}: "{str(cpe)}".  Traceback: "{exception_traceback}".'
        )
        logger.warning(exception_message)

    return status_code