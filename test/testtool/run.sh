#/bin/bash

cd $(dirname $0)

. ../task.info
. ../controller.info



python multioutput.py $inputFile >> report.log
echo "over" >> report.log
