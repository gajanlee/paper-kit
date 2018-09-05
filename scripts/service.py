#!/usr/bin/python3

# This module will expose interface as a RESTful server.

import json
import os
import bottle
from bottle import route, run, request

DIR_PATH = "./"
files = [path for path in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, path))]

app = bottle.Bottle()

# return html page's content, maybe basepath should't in the parameter
def html_page(path):
    with open(path) as fp:
        return fp.read()

@app.get("/")
def main_page():
    return html_page("../pages/tags.html")

@app.get("/files")
def get_files():
    return {"files": files}

@app.get("/content")
def get_file_content():
    global files
    with open(os.path.join(DIR_PATH, files[int(request.query.file_id)])) as fp:
        return {"content": fp.read()}

@app.route("/amend", method="PATCH")
def amend_file():
    body = json.load(request.body)

    with open(os.path.join(DIR_PATH, files[int(request.query.file_id)]), "w") as fp:
        fp.write(body["content"])
        return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=8081, host="0.0.0.0")