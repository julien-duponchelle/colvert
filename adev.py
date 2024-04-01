#
# This script is wrapper on top of aiohttp-devtools
# to allow to use a debugger and reload the server
#

import os

from aiohttp_devtools.cli import cli

if __name__ == "__main__":
    # Setup env variable
    os.environ["AIO_APP_FACTORY"] = "create_app"
    os.environ["AIO_ROOT"] = os.getcwd()
    os.environ["AIO_APP_PATH"] = "colvert/demo.py"
    cli()