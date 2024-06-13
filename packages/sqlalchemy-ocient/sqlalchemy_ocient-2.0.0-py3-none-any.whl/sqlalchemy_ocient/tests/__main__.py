import os
import sys
from pathlib import Path

import pytest

"""
This file allows `python -m sqlalchemy_ocient.tests` to run the sqlalchemy
pytest suite
"""

dir_path = os.path.dirname(os.path.realpath(__file__))

cmd = [dir_path + "/test_suite.py"]

# The following checks are for the internal Bazel test environment
if "TESTBRIDGE_TEST_ONLY" in os.environ:
    cmd = cmd + ["-k", os.environ["TESTBRIDGE_TEST_ONLY"]]

if "BAZEL_TEST" in os.environ:
    cmd = cmd + ["--override-ini=cache_dir=" + os.environ["TEST_TMPDIR"]]

if len(sys.argv) > 0:
    cmd.extend(sys.argv[1:])

sys.exit(pytest.main(cmd))
