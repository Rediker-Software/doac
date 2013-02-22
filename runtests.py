import os
import sys

sys.path.insert(0, os.getcwd())

from django.conf import settings
from tests import settings as test_settings

settings.configure(test_settings, debug=True)

from django.test.utils import get_runner

TestRunner = get_runner(settings)

runner = TestRunner(verbosity=1, interactive=False, failfast=True)

runner.run_tests(["tests", ])
