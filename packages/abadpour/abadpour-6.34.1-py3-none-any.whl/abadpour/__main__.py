import argparse
from abadpour import NAME, VERSION
from abadpour.build import build
from abadpour.logger import logger

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="build|version",
)
args = parser.parse_args()

success = False
if args.task == "build":
    success = build()
elif args.task == "version":
    print(f"{NAME}-{VERSION}")
    success = True
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
