bind = "0.0.0.0:80"
accesslog = "/data/gunicorn.log"
errorlog = "/data/gunicorn_error.log"
workers = 4
worker_class = "gevent"
threads = 2
