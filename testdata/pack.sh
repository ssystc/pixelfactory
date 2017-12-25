# /bin/bash

cd $(dirname $0)

rm -rf trans
mkdir trans
cp run.sh trans
cp trans.py trans
cp sptrans trans
cp -r lib trans
tar -zcvf trans.tar.gz trans
cp trans.tar.gz ~/framework/testTools/
