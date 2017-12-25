# /bin/bash

cd $(dirname $0)
curdir = &(pwd)
echo $curdir

. ../task.info
. ../controller.info

SO_PATH=$curdir/lib

if [ $LD_LIBRARY_PATH ];then
	LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SO_PATH
else
	LD_LIBRARY_PATH=$SO_PATH
fi

echo "begin trans" >> report.log
python trans.py $configFile >> report.log
echo "end trans" >> report.log

