import os.path
from subprocess import getoutput
from django.contrib.staticfiles.management.commands import collectstatic
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--type', action='store', default=None,
            dest='type', metavar='<js|css>',
            help="Only minify this type of static files")
        parser.add_argument('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the filesystem.")

    def _minify(self, extension):
        for root, dirs, files in os.walk(settings.STATIC_ROOT):
            for f in files:
                path = os.path.join(root, f)
                if path.endswith(extension):
                    if getattr(self, 'dry_run', False):
                        print('[dry run] skipping minifying ' + path + '...')
                        continue
                    mini = getoutput('yui-compressor ' + path)
                    print('minifying "' + path + '" ... ', end='')
                    with open(path, 'w') as p:
                        p.write(mini)
                    print('done')

    def set_options(self, **options):
        """
        Set instance variables based on an options dict
        """
        self.type = options['type']
        self.dry_run = options['dry_run']

    def handle(self, **options):
        self.set_options(**options)
        print(self.type)
        if self.type is not None:
            self._minify(self.type)
        else:
            self._minify('css')
            self._minify('js')
