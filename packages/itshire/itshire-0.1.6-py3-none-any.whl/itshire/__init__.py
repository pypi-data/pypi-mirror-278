import logging

from . import add_sections, cli, log

__project_name__ = "itshire"


def main() -> int:
    args = cli.parse_args()
    log.configure_logging(args.verbose)
    logging.debug("fart")

    if args.command == "addstores":
        add_sections.main()
    else:
        print("hello")

    return 0
