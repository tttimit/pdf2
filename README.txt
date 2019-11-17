依赖：
1、命令行工具 qpdf，用来解密，需要下载安装： https://github.com/qpdf/qpdf
2、读写pdf的 Python 库 pdfrw: https://github.com/pmaupin/pdfrw
3、用来 flatten PDF 文件的 pypdftk： 尚未完全解决 flatten 的问题，貌似 Windows 没有好办法

存在问题：
1、通过 pdfrw 自动填写的字段，在 Adobe Acrobat Reader DC 中无法默认显示。
    https://github.com/pmaupin/pdfrw/issues/84
    workaround： https://github.com/pmaupin/pdfrw/issues/84#issuecomment-463493521
   通过浏览器打开可以正确显示大部分字段，但是对于 checkbox、date、textarea 显示支持的不好。
   其中 date 和 textarea 即使在 Adobe 浏览器中直接填写，显示的效果也很糟糕。

2、Flatten问题，查看了若干解决方案，比如设置 acroform 的 Ff 属性为1，不起作用：
    https://stackoverflow.com/a/33879924

    使用 pypdftk，在windows下支持不好，命令会报错，还未找到解决方案：
    https://stackoverflow.com/questions/27023043/generate-flattened-pdf-with-python
    https://github.com/mikehaertl/php-pdftk/issues/62#issuecomment-261182787
