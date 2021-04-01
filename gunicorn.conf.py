import os

proc_name = "adrsir-api"

accesslog = "log/access.log"
errorlog = "log/error.log"

bind = "127.0.0.1:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = 1

debug = os.environ.get("DEBUG", "false") == "true"
reload = debug
preload_app = False
daemon = False
