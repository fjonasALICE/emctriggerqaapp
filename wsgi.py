#! /usr/bin/env python3
import os

from webapp.app import app

DATAREPO=os.environ["DATAPATH"]

application = app

application.static_folder = DATAREPO
application.static_url_path = "/static"
application.run(host="0.0.0.0", port=8080)
