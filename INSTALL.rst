==========================
Main site Django_ project
==========================

.. image:: https://img.shields.io/travis/alphageek-xyz/site.svg?style=flat-square
	:target: https://travis-ci.org/alphageek-xyz/site
	:alt: Build status

.. image:: https://img.shields.io/coveralls/alphageek-xyz/site.svg?style=flat-square
	:target: https://coveralls.io/github/alphageek-xyz/site
	:alt: Coveralls status

.. image:: https://img.shields.io/github/tag/alphageek-xyz/site.svg?style=flat-square
        :target: https://github.com/alphageek-xyz/site/releases/latest
        :alt: Tag

.. image:: https://img.shields.io/github/license/alphageek-xyz/site.svg?style=flat-square
        :target: https://github.com/alphageek-xyz/site/blob/master/LICENSE
        :alt: License

.. _Django: https://www.djangoproject.com/

The code provided in this repo will not run flawlessly without local modification and additional configuration; however, some parts may be useful references. Feel free to use it as a starting point for your own website.

To run locally, do the following (on Ubuntu 16.04):

#. Install system dependencies.

   .. code-block:: bash

    sudo apt-get install git python3-dev python3-pip \
        postgresql-9.5 postgresql-server-dev-9.5
    sudo -H pip3 install -U pip virtualenvwrapper

#. Create a data directory and ``secrets.json``.

   .. code-block:: bash

    mkdir -p ~/data/conf && echo '
    { "secret_key": "xyz",
      "db_host": "localhost",
      "db_password": "db-secret",
      "gapi_key": "gapi-secret",
      "recaptcha_pri": "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",
      "recaptcha_pub": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
      "email_host_user": "foo@example.com",
      "email_host_pass": "email-secret" }
    ' > ~/data/conf/secrets.json

#. Set environment variables.

   .. code-block:: bash

     cat <<EOF>> ~/.bashrc && . ~/.bashrc
     set -a
     VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
     DJANGOPROJECT_DATA_DIR=~/data
     set +a
     . /usr/local/bin/virtualenvwrapper.sh
     EOF

#. Configure the database.

   .. code-block:: sql

    cat <<EOF | sudo -u postgres psql
    DROP DATABASE IF EXISTS agcs_db;
    CREATE DATABASE agcs_db;
    DO \$$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'django') THEN
            CREATE ROLE django WITH CREATEDB PASSWORD '$(python3 -c \
                "import sys; exec('\n'.join(sys.argv[1:]))" "import json" \
                "with open('$DJANGOPROJECT_DATA_DIR/conf/secrets.json') as f:" \
                " print(json.load(f)['db_password'])")';
        END IF;
    END \$$;
    ALTER ROLE django SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE agcs_db TO django;
    EOF

#. Create a Python 3.x virtualenv.

   .. code-block:: bash

    mkvirtualenv -p python3 agcs

#. Clone this repository.

   .. code-block:: bash

    mkdir ~/site && cd ~/site
    git clone https://github.com/alphageek-xyz/site.git
    cd site && setvirtualenvproject

#. Install dependencies and run tests.

   .. code-block::

    make install && make test

#. Generate favicons and collect static files.

   .. code-block:: bash

        make static

#. Populate the database with some defaults.

   .. code-block:: bash

    make load

#. Run the development server.

   .. code-block:: bash

    make run

- Note: If you are modeling your own site after this one, the following steps will help ensure compliance with condition #3 of the LICENSE
    + Adjust all brand-related variables and settings
    + Use your own logo
    + Use your own fixtures
