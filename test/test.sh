#!/bin/bash
script_dir=$(dirname $(readlink -f $0))

cd $script_dir

rm -rf ./test0
rm -rf ./test1
rm -rf ./test2

# 复制文件
mkdir test0
cp -r ./bak/* ./test0
mkdir test1
cp -r ./bak/* ./test1
mkdir test2
cp -r ./bak/* ./test2

# 测试脚本
python ../src/cwebp4md.py ./test0/test.md -d ./test0/d/ -r ./test0/r/

python ../src/cwebp4md.py ./test1/test.md -d ./test1/d/ -r ./test1/r/ --replace

../dist/cwebp4md.exe ./test2/test.md -d ./test2/d/ -r ./test2/r/
