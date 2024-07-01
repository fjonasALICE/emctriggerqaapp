#! /usr/bin/env python3
import os

from app import app

DATAREPO=os.environ["DATAPATH"]

if __name__ == "__main__":
    app.static_folder = DATAREPO
    app.static_url_path = "/static"
    app.run(host="0.0.0.0")