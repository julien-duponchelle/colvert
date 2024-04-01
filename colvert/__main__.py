import logging

from colorama import Fore, init

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        if record.levelno == logging.INFO:
            record.msg = Fore.GREEN + str(record.msg)
        elif record.levelno == logging.WARNING:
            record.msg = Fore.YELLOW + str(record.msg)
        elif record.levelno == logging.ERROR:
            record.msg = Fore.RED + str(record.msg)
        elif record.levelno == logging.CRITICAL:
            record.msg = Fore.RED + str(record.msg)
        elif record.levelno == logging.DEBUG:
            record.msg = Fore.BLUE + str(record.msg)
        return logging.Formatter.format(self, record)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    # Reset log handlers to avoid duplicate messages
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    handler.setFormatter(ColorFormatter("%(asctime)s %(message)s", datefmt="%H:%M:%S"))

    from .cli import cli

    cli()


if __name__ == "__main__":
    main()