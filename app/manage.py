#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":

    if 'test' in sys.argv and sys.argv.index('test') == 1:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        if ('-p' or '--pattern') not in sys.argv:
            sys.argv.insert(2, '-p')
            sys.argv.insert(3, '*.py')
        if 'tests' not in sys.argv:
            sys.argv.append('tests')
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agcs.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
