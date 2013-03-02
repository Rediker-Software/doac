from argparse import ArgumentParser
import sys

parser = ArgumentParser(description="Run the test suite.")

parser.add_argument(
    "--failfast",
    action="store_true",
    default=False,
    dest="failfast",
    help="Stop the test suite after the first failed test.",
)

parser.add_argument(
    "--no-coverage",
    action="store_false",
    default=True,
    dest="coverage",
    help="Do not run coverage.py while running the tests.",
)

parser.add_argument(
    "--no-input",
    action="store_false",
    default=True,
    dest="interactive",
    help="If the tests require input, do not prompt the user for input.",
)

args = parser.parse_args()

if args.coverage:
    try:
        from coverage import coverage

        cov = coverage(omit="tests*")
        cov.start()
    except ImportError:
        cov = None
else:
    cov = None

from django.conf import settings
from tests import settings as test_settings

settings.configure(test_settings, debug=True)

from django.test.utils import get_runner

TestRunner = get_runner(settings)

runner = TestRunner(verbosity=1, interactive=args.interactive, failfast=args.failfast)

failures = runner.run_tests(["tests", ])

if cov:
    cov.stop()
    cov.html_report()

if failures:
    sys.exit(bool(failures))
