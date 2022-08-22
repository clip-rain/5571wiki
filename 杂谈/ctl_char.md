# 控制字符
## 一、什么是控制字符
控制字符是计算机系统中不可打印的一类字符。它们用于控制系统的动作。例如BS是将光标会退一格的控制字符。

## 二、控制字符表
https://www.geeksforgeeks.org/control-characters/



## 三、如何在文件中插入控制字符
经过多次测试，找到一种可行的办法：
echo [control] + [V] + [H] > text.txt<br>
[control] + [V] + [H]也是目前唯一找到能在控制台打印出控制字符BS的方法。
[control] + [H] 在控制台中会直接执行。