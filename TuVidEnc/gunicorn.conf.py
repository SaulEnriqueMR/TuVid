# Don't use port 80 becaue nginx occupied it already.
bind = "127.0.0.1:9001"
# Make sure you have the log folder create
errorlog = '/home/saule/tuvidenv/logs/gunicorn-error.log'
accesslog = '/home/saule/tuvidenv/logs/gunicorn-access.log'
loglevel = 'debug'
workers = 9     # the number of recommended workers is '2 * number of CPUs + 1'
