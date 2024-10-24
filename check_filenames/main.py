import argparse
import re
from pathlib import Path
from typing import Sequence

import logging

import yaml

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


def main(*argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to run")
    parser.add_argument("-r", "--regex", action="store", dest="regex")
    args = parser.parse_args(*argv)

    if not args.filenames:
        return 0

    if not args.regex:
        logger.warning("""No regex submitted, add "args: ['-r <regex>']" to you pre-commit hook""")
        return 0

    regex = re.compile(args.regex.strip())

    bad_files = [filename for filename in args.filenames if not regex.match(Path(filename).stem)]

    if bad_files:
        logger.error(
            f"The following file{'' if len(bad_files) == 1 else 's'} have name that dones't match "
            f"the provided regex ({regex.pattern}):\n{yaml.dump(bad_files, indent=2)}"
        )
        return len(bad_files)


if __name__ == "__main__":
    raise SystemExit(main())
