import asyncio
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import importlib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def load_all_extensions():
    for dir in os.listdir("./extends"):
        # run pip install -r requirements.txt if exists
        if os.path.exists("./extends/" + dir + "/requirements.txt"):
            try:
                print("pip install -r ./extends/" + dir + "/requirements.txt")
                os.system("pip install -r ./extends/" + dir +
                          "/requirements.txt")
            except:
                print("pip install -r ./extends/" + dir +
                      "/requirements.txt failed")
        for file in os.listdir("./extends/" + dir):
            if file.endswith(".py") and not file.startswith("_"):
                try:
                    print(dir + "/" + file)
                    # dynamic import
                    tmp = importlib.import_module("extends." + dir + "." +
                                                  file[:-3])
                    app.include_router(tmp.router)
                except Exception as e:
                    print("Failed to load import {0}.".format(file))
                    print(e)
                    print(''.join(traceback.format_exception(None, e, e.__traceback__)))


load_all_extensions()
