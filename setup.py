import multiprocessing

bind = "127.0.0.1"
workers = multiprocessing.cpu_count()
errorlog = '-'
accesslog = '-'
access_log_format = "%(h)s %(q)s %(U)s %(s)s %(b)s"