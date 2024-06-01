# 将Markdown中的本地图片转换成webp格式

[WebP](https://developers.google.com/speed/webp)的设计目标是在减少文件大小的同时，达到和[JPEG](https://zh.wikipedia.org/wiki/JPEG)、[PNG](https://zh.wikipedia.org/wiki/PNG)、[GIF](https://zh.wikipedia.org/wiki/GIF)格式相同的图片质量，并希望借此能够减少图片档在网络上的发送时间。

因为个人博客使用markdown写的，希望图片尽量小一点，所以就写了一个python脚本来自动转化图片。

该脚本搜索markdown中引用的本地图片，把图片压缩成同名的.webp格式，注释markkdown中的原来的图片引用，并添加新的图片引用。

## ！！！ 注意事项

这个脚本是用正则表达式实现的，所以可能由很多漏洞。

其实这种功能适合在构建网页的时候实现，然而我并不会ts js之类的。

已经修复的问题：
- 代码块中的图片链接不会处理
- 注释掉的图片链接不会处理

## 使用方法

```shell
python cwebp4md.py <input_file_pattern> [-r <directory>] [-d <directory>] [--replace] [-h | --help]
```

可选的输入参数
- `-r <directory>`: 递归搜索`<directory>`及其子目录中的.md文件并处理
- `-d <directory>`: 处理`<directory>`下的.md文件
- `<file>` ：处理指定文件，支持通配符
- `--replace`: 替换原链接，而不是默认的注释旧链接在添加新链接

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

## pyinstaller 打包

```
pyinstaller ./cwebp4md.spec
```



## 效果

<details>
    <summary>点击展开</summary>

# 测试案例

## 会触发替换的情况
测试案例，首先是一个被文本包围的GIF <!-- ![gif](./assets/gif.gif) --> ![gif](./assets/gif.webp)，替换gif

PNG测试
<!-- ![a](./assets/png.png) --> ![a](./assets/png.webp)

JPG测试
<!-- ![b](./assets/jpg.jpg) --> ![b](./assets/jpg.webp)


## 不会触发替换的情况

1. 代码中的图片应该不被处理

```
![a](./assets/png.png)
```


2. 注释不会处理
   <!-- ![a](./assets/png.png) -->

3. 注释中间包含其他字符也不会被处理
    <!-- ![b](./assets/jpg.jpg)  ![b](./assets/jpg.jpg) -->

4. webp格式不会处理 
   ![a](./assets/png.webp)

5. 并不是图片引用的格式不会被替换
    ./assets/jpg.jpg

6. 不存在的图片也不会被替换
    ![a](./assets/不存在的图片.jpg)

</details>
