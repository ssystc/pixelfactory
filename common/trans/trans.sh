# /bin/bash

CURDIR=$(cd $(dirname $0);pwd)
SOPATH=$CURDIR/lib
if [ $LD_LIBRARY_PATH ];then
    LD_LIBRARY_PATH=$SOPATH:$LD_LIBRARY_PATH
else
    LD_LIBRARY_PATH=$SOPATH
fi
export LD_LIBRARY_PATH

chmod +x $CURDIR/sptrans
$CURDIR/sptrans $1 $2 $3
