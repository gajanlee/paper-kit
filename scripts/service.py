#!/usr/bin/python3

# This module will expose interface as a RESTful server.

import os
import bottle
from bottle import route, run, request

DIR_PATH = "./"
files = [path for path in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, path))]

app = bottle.Bottle()

@app.get("/")
def main_page():
    with open("../pages/tags.html") as fp:
        return fp.read()

@app.get("/files")
def get_files():
    return {"files": files}

@app.get("/content")
def get_file_content():
    global files
    with open(os.path.join(DIR_PATH, files[int(request.query.file_id)])) as fp:
        return {"content": fp.read()}

if __name__ == "__main__":
    app.run(port=8081, host="0.0.0.0")