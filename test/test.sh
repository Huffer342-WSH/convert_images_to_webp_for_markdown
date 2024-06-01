#!/bin/bash
script_dir=$(dirname $(readlink -f $0))

cd $script_dir

rm -rf ./test
rm -rf ./test2

# 复制文件
mkdir test
cp -r ./bak/* ./test
mkdir test2
cp -r ./bak/* ./test2

# 测试脚本
# python ../src/cwebp4md.py ./test/test.md -d ./test/d/ -r ./test/r/
python ../src/cwebp4md.py ./test/test.md 

# ../dist/cwebp4md.exe ./test2/test.md -d ./test2/d/ -r ./test2/r/
