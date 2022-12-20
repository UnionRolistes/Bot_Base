from fastapi import FastAPI
import os
import importlib

import logging
from fastapi.logger import logger as fastapi_logger

# get print of python in docker
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handle
fastapi_logger.handlers = gunicorn_error_logger.handle
if __name__ != "__main__":
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)

app = FastAPI()


def load_all_extensions():
    for dir in os.listdir('./extends'):
        # run pip install -r requirements.txt if exists
        if os.path.exists('./extends/'+dir+'/requirements.txt'):
            try:
                print('pip install -r ./extends/'+dir+'/requirements.txt')
                os.system('pip install -r ./extends/'+dir+'/requirements.txt')
            except:
                print('pip install -r ./extends/' +
                      dir+'/requirements.txt failed')
        for file in os.listdir('./extends/'+dir):
            if file.endswith('.py'):
                try:
                    print(dir+'/'+file)
                    # dynamic import
                    tmp = importlib.import_module('extends.'+dir+'.'+file[:-3])
                    app.include_router(tmp.router)
                except Exception as e:
                    print('Failed to load import {0}.'.format(file))
                    print(e)


load_all_extensions()

# app.include_router(users.router)
