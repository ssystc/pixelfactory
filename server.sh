# /bin/bash

CUR_DIR=$(dirname $0)

cd CUR_DIR

cd ..

source env/bin/active

cd CUR_DIR

python runtaskserver.py > ./log/task.log 2>&1 &

gunicorn -b 0.0.0.0:8283 --error-logfile ./log/error.log --access-logfile ./log/access.log --log-level debug runwebserver:app > /dev/null 2>&1 & 
