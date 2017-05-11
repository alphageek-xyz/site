import subprocess

def set_headers(response, default=True, **headers):
    for header,value in headers.items():
        h = header.replace('_', '-')
        if default:
            response.setdefault(h, value)
        else:
            response[h] = value


def del_headers(response, *headers):
    for header in headers:
        h = header.replace('_', '-')
        if response.has_header(h):
            del(response[h])


def get_uwsgi_version():
    status, output = subprocess.getstatusoutput(['uwsgi --version'])
    return None if status else output


def get_gunicorn_version(): # pragma: no cover
    try:
        from gunicorn import __version__
        return __version__
    except ImportError:
        return None
