#!/usr/bin/env python

import os, sys
import django
from pathlib import Path
from django.conf import settings
from django.test.utils import get_runner


def main():
    if 'test' not in sys.argv:
        sys.argv.insert(1, 'test')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    os.environ.setdefault('DJANGOPROJECT_DATA_DIR', str(
        Path(__file__).resolve().parent.joinpath('tests', 'data')
    ))

    if len(sys.argv) == 1:
        django.setup()
        TestRunner  = get_runner(settings)
        test_runner = TestRunner()
        failures    = test_runner.run_tests(['tests'])
        sys.exit(bool(failures))
    main()
