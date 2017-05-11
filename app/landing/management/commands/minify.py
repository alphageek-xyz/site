import os, sys
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.management.base import BaseCommand
from django.conf import settings
from css_html_js_minify import minify


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
            help="Do everything except modify the filesystem.", default=False)
        parser.add_argument('--clear', action='store_true',
            help="Clear static files.", default=False)
        parser.add_argument('--wrap', action='store_true',
            help="Wrap output to ~80 chars per line, CSS only.")
        parser.add_argument('--prefix', type=str,
            help="Prefix string to prepend on output filenames.")
        parser.add_argument('--timestamp', action='store_true',
            help="Add a Time Stamp on all CSS/JS output files.")
        parser.add_argument('--quiet', action='store_true',
            help="Quiet, Silent.")
        parser.add_argument('--hash', action='store_true',
            help="Add SHA1 HEX-Digest 11chars Hash to Filenames.")
        parser.add_argument('--zipy', action='store_true',
            help="GZIP Minified files as '*.gz', CSS/JS only.")
        parser.add_argument('--sort', action='store_true',
            help="Alphabetically Sort CSS Properties, CSS only.")
        parser.add_argument('--comments', action='store_true',
            help="Keep comments, CSS/HTML only (Not Recommended)")
        parser.add_argument('--overwrite', action='store_true',
            help="Force overwrite all in-place (Not Recommended)")
        parser.add_argument('--after', type=str,
            help="Command to execute after run (Experimental).")
        parser.add_argument('--before', type=str,
            help="Command to execute before run (Experimental).")
        parser.add_argument('--watch', action='store_true',
            help="Watch changes.")
        parser.add_argument('--multiple', action='store_true',
            help="Allow Multiple instances (Not Recommended).")
        parser.add_argument('--beep', action='store_true',
            help="Beep sound will be played when it ends at exit.")

    def collectstatic(self, clear):
        args = ['', 'collectstatic', '--noinput']
        clear and args.append('--clear')
        collectstatic.Command().run_from_argv(args)

    def execute(self, *args, **kwargs):
        self.collectstatic(kwargs.get('clear', False))
        try:
            sys.argv.pop(sys.argv.index('--clear'))
        except ValueError:
            pass
        sys.argv = [''] + sys.argv[2:]
        sys.argv.append(settings.STATIC_ROOT)
        minify.prepare()
        minify.main()
