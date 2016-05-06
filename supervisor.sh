!/bin/bash
source env/bin/activate
gunicorn ImageGenerater.wsgi:application -c gunicorn.conf
