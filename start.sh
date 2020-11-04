#!/bin/bash

docker run -it --rm -v $1:/opt/inputs -v $(pwd)/logs:/opt/logs -v $(pwd)/outputs arthurtibame/sql_upload:0.0.2 python3 /opt/main.py --input /opt/inputs --type $2
