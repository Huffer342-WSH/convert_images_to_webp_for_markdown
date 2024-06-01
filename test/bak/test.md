# 测试案例

## 会触发替换的情况
测试案例，首先是一个被文本包围的GIF ![gif](./assets/gif.gif)，替换gif

PNG测试
![a](./assets/png.png)

JPG测试
![b](./assets/jpg.jpg)


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
