import multiprocessing

bind = "192.168.33.10:8000"
workers = multiprocessing.cpu_count()
loglevel = 'info'
errorlog = '-'
accesslog = '-'
access_log_format = "%(h)s %(q)s %(U)s %(s)s %(b)s"