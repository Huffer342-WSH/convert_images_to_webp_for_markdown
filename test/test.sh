#!/bin/bash
script_dir=$(dirname $(readlink -f $0))

cd $script_dir

# 复制文件
mkdir test
cp -r ./bak/* ./test

# 测试脚本
# python ../src/cwebp4md.py ./test/test.md -d ./test/d/ -r ./test/r/

../dist/cwebp4md.exe ./test/test.md -d ./test/d/ -r ./test/r/
