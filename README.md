# 将Markdown中的本地图片转换成webp格式

[WebP](https://developers.google.com/speed/webp)的设计目标是在减少文件大小的同时，达到和[JPEG](https://zh.wikipedia.org/wiki/JPEG)、[PNG](https://zh.wikipedia.org/wiki/PNG)、[GIF](https://zh.wikipedia.org/wiki/GIF)格式相同的图片质量，并希望借此能够减少图片档在网络上的发送时间。

因为个人博客使用markdown写的，希望图片尽量小一点，所以就写了一个python脚本来自动转化图片。

该脚本搜索markdown中引用的本地图片，把图片压缩成同名的.webp格式，并修改markdown中引用的图。

## 使用方法

```shell
python cwebp4md.py <input_file_pattern> [-r <directory>] [-d <directory>] [-h | --help]
```

可选的输入参数
- `-r <directory>`: 递归搜索`<directory>`及其子目录中的.md文件并处理
- `-d <directory>`: 处理`<directory>`下的.md文件
- `<file>` ：处理指定文件，支持通配符

## 测试

[./test/test.sh](./test/test.sh)
该脚本把测试文件复制到`./test`目录下，然后执行python脚本

```shell
#!/bin/bash
script_dir=$(dirname $(readlink -f $0))

cd $script_dir

# 复制文件
mkdir test
cp -r ./bak/* ./test

# 测试脚本
python ../src/cwebp4md.py ./test/test.md -d ./test/d/ -r ./test/r/

```
