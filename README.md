# WebFont serperator

## 简介/注意事项
* 由于中文的字体文件包含非常多的字符，因此字体文件往往非常大；`Google Fonts`给出了相当不错的解决方案：由于`CSS`支持为同一个字体的不同部分指定不同的字体文件，在加载网页时按需加载，因此可以将字体事先做好字符子集化，并设置好相应的`CSS`文件，这样在加载网页时即可尽量减少消耗不必要的网络流量了。
* `Google Fonts`给出的`API`的例子有：[Noto Sans SC](https://fonts.googleapis.com/css?family=Noto+Sans+SC), [Noto Sans JP](https://fonts.googleapis.com/css?family=Noto+Sans+JP)
* 然而，`Noto Sans`(同`Adobe`的`Source Han Sans`系列) 在网页上上的渲染效果并没有(`Sarasa Gothic`)[https://github.com/be5invis/Sarasa-Gothic]好，因此出于替换用目的，我写了此工具用于分割更纱黑体以取代谷歌提供的`Web Font`；如果您手上有其他字体需要进行分割，也可以使用此工具；
* 由于我个人并没有技术像谷歌那样计算好怎么分割字体比较合适，每个字体需要哪些字形，因此此工具参照了谷歌的`CSS`文件，完全按照谷歌的分割方式进行分割，在使用时需在本地导入一份谷歌的`CSS`样式文件；当然如果您手上有别的分割方法，也可以将其写入一个`CSS`文件中进行导入；或者如果您有别的更好的方式进行分割，欢迎`Pull Request`
* 请务必使用对应地区化字形的分割方式，例如，
* 本工具设计的时候只考虑了谷歌的`CSS`格式，即以正则表达式`(?<=unicode-range: ).+?(?=;)`进行匹配，如果您本地想要导入的`CSS`文件中的冒号后并无空格，请手动删除
* 本工具基于`Python`的`fonttools`中的`pyftsubset`
* 请注意，`CSS`支持对一个字体设置`Normal`和`Italic`两种样式，而本工具一次只能对其中一种进行处理；如需对两种样式都进行处理，请修改设置运行两次

## 使用方法
1. 请先安装`fonttools`:
```
pip install fonttools
```
2. 然后，请确保`pyftsubset`所在的文件夹在您的系统的`环境变量 Path`中
3. 将您需要应用的分割方式的`CSS`文件从`Google Fonts`上下载下来并保存在本地
4. 准备您需要使用的字体文件
5. 使用文本编辑器打开`py`文件，在文件开头处填写好相关设置
6. 运行本工具
7. 将生成结果上传至您的服务器，应用在网页中
