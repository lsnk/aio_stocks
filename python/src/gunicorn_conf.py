import multiprocessing


bind = '0.0.0.0:8000'

cores = multiprocessing.cpu_count()
workers_per_core = 1
workers = int(cores * workers_per_core)

worker_class = 'uvicorn.workers.UvicornWorker'
