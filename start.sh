#!/bin/bash

docker run -it --rm -v $1:/opt/inputs arthurtibame/sql_upload:0.0.1 python3 /opt/main.py --input /opt/inputs --type $2
