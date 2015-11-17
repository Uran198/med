Deploy
========

Bad guide - no automation :(
----------------------------

###Initial server configuration

1. `ssh` into your server::

   $ ssh root@xxx.xxx.xxx.xxx

2. Update your system::

        $ aptitude update
        $ aptitude upgrade

3. Create a user for your app and assign to a system group `webapps` (it's dangerous running things like root)::

        $ groupadd --system webapps
        $ useradd --system --gid webapps --shell /bin/bash --home /django/<username> <username>

4. Install git, create users home directory and clone your project::

        $ aptitude install git
        $ mkdir -p /django/<username>
        $ cd /django/<username>
        $ git clone https://github.com/<Account>/<project.git>
        $ chown --recursive <username> /django/<username>

5. Install os dependencies::

        $ cd /django/<username>/<project>/
        $ ../install_os_dependencies.sh

6. If you want to have database on the same server with your application, do the following::
    1. Install postgresql::

        $ aptitude install postgresql postgresql-contrib

    2. Configure postgresql::

        $ su - postgres
        $ createuser <username> # not sure this is necessary
        $ createdb <project>
        $ psql
        postgres=# ALTER DATABASE <project> OWNER TO <username>;

7. As an application user install virtualenv, activate it and install all the dependencies::

        $ su - <username>
        $ virtualenv --python=python3.4 .
        $ source bin/activate
        $ cd <project>/
        $ pip install -r requirments.txt

8. Set enviroment variables, see `env.example`. I created file which could be sourced
9. Run migrations and collectstatic::

        $ cd /django/<username>/<project>/
        $ ./manage.py migrate
        $ ./manage.py collectstatic

10. At this point you should be able to start server with gunicorn (if for some reason it's not the case, try to solve it and correct here)::

        $ gunicorn config.wsgi:application --bind <domain> <port>

11. add `bin/gunicorn_start` of content:
::

     #!/bin/bash

     NAME="<project>"                                      # Name of the application
     DJANGODIR=/django/<username>/<project>                # Django project directory
     SOCKFILE=/django/<username>/run/gunicorn.sock         # we will communicte using this unix socket
     USER=<username>                                       # the user to run as
     GROUP=webapps                                         # the group to run as
     NUM_WORKERS=3                                         # how many worker processes should Gunicorn spawn
     DJANGO_SETTINGS_MODULE=config.settings.production     # which settings file should Django use
     DJANGO_WSGI_MODULE=config.wsgi                        # WSGI module name

     echo "Starting $NAME as `whoami`"

     # Activate the virtual environment
     cd $DJANGODIR
     source ../bin/activate
     source <env                                           # file with your enviroment exports
     export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
     export PYTHONPATH=$DJANGODIR:$PYTHONPATH

     # Create the run directory if it doesn't exist
     RUNDIR=$(dirname $SOCKFILE)
     test -d $RUNDIR || mkdir -p $RUNDIR

     # Start your Django Unicorn
     # Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
     exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
     --name $NAME \
     --workers $NUM_WORKERS \
     --user=$USER --group=$GROUP \
     --bind=unix:$SOCKFILE \
     --log-level=debug \
     --log-file=-

12. Install supervisor::

        $ aptitude install supervisor

13. Configure supervisor task in `/etc/supervisor/conf.d/<project>.conf`:
::

    [program:<project>]
    command = /django/<username>/bin/gunicorn_start                       ; Command to start app
    user = <username>                                                     ; User to run as
    stdout_logfile = /django/<username>/logs/gunicorn_supervisor.log      ; Where to write log messages
    redirect_stderr = true                                                ; Save stderr in the same log
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding

14. Create a file to store logs in::

    $ mkdir -p /django/<username>/logs/
    $ touch /django/<username>/logs/gunicorn_supervisor.log

15. Make supervisor reread configuration and update::

    $ supervisorctl reread
    $ supervisorctl update

16. Setting up nginx::

    $ aptitude install nginx

17. Create configuration file for nginx `/etc/nginx/sites-available/<project>`:
::

    upstream <project>_app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response (in case the Unicorn master nukes a
    # single worker for timing out).

    server unix:/django/<username>/run/gunicorn.sock fail_timeout=0;
    }

    server {

        listen   80;
        server_name medvoloc.tk;

        client_max_body_size 4G;

        access_log /django/<username>/logs/nginx-access.log;
        error_log /django/<username>/logs/nginx-error.log;

        # location /media/ {
        #     alias   /webapps/hello_django/media/;
        # }

        location / {
            # an HTTP header important enough to have its own Wikipedia entry:
            #   http://en.wikipedia.org/wiki/X-Forwarded-For
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # enable this if and only if you use HTTPS, this helps Rack
            # set the proper protocol for doing redirects:
            # proxy_set_header X-Forwarded-Proto https;

            # pass the Host: header from the client right along so redirects
            # can be set properly within the Rack application
            proxy_set_header Host $http_host;

            # we don't want nginx trying to do something clever with
            # redirects, we set the Host: header above already.
            proxy_redirect off;

            # set "proxy_buffering off" *only* for Rainbows! when doing
            # Comet/long-poll stuff.  It's also safe to set if you're
            # using only serving fast clients with Unicorn + nginx.
            # Otherwise you _want_ nginx to buffer responses to slow
            # clients, really.
            # proxy_buffering off;

            # Try to serve static files from nginx, no point in making an
            # *application* server like Unicorn/Rainbows! serve static files.
            if (!-f $request_filename) {
                proxy_pass http://<project>_app_server;
                break;
            }
        }

        # Error pages
        # error_page 500 502 503 504 /500.html;
        # location = /500.html {
        #     root /webapps/hello_django/static/;
        #}
    }

18. Create symbolic link and delete default::

    $ ln -s /etc/nginx/sites-available/<project> /etc/nginx/sites-enabled/<project>
    $ rm /etc/nginx/sites-enabled/default

19. Restart nginx::

    $ service nginx restart

20. Congradulate yourself!


NOTE::
    When you will need to change `Site` model make sure that new object has an id that's equal to SITE_ID in your settnigs(in my case 1)
