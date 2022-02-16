# <center>python依赖包的一些分析</center>
### 背景
项目中有一个pymysql的module。用pycharm在site-packages中可以看到有两个dist-info中的顶级目录中包含有pymysql。它们分别是PyMySQL和PyMySQL_shopee。那么问题来了，项目中实际使用的pymysql是来自于哪个呢？
注：site-packages包含了所有安装好的package。package有两部分信息，一部分是dist-info，即package的元信息；另一部分是package中包含的module。理论上一个package可以包含有多个module，在package的元信息中的top_level.txt可以看到其包含的modules。

### 探究
1、PyMySQL_Shopee和PyMySQL之间的关系是什么？
- 首先创建一个干净的python环境。
- 然后用pip install PyMySQL_shopee。得到的结果是增加了两个modules，分别是MySQLdb和pymysql。
- 再pip uninstall PyMySQL_shopee。去掉这个package。
- 再pip install pymysql。得到了一个moudle，即pymsql。
- 对比这一次的pymysql和上一次的pymysql的不同，发现仅仅是版本不一致。实际代码是一样的。
- 查看PyMySQL_Shopee的元信息中的METADATA和RECORD，发现PyMySQL_Shopee是直接包含了pymsql代码的，并不是通过依赖而建立的关系。

综上，PyMySQL_Shopee是把pymsql的某个版本直接拷贝到了自己的项目中作为一个module而存在的。而PyMySQL则是pymysql这个module的原始项目

2、PyMySQL_Shopee和PyMySQL二者的安装顺序会有区别吗？

- 先装PyMySQL_Shopee，后装PyMySQL，最后pymsql这个module一定来自后安装的PyMySQL。
- 先装PyMySQL，后装PyMySQL_Shopee，最后pymsql这个module一定来自后安装的PyMySQL_Shopee。

综上，module名字相同，但是来自不同的package的情况下，那么后面安装的会覆盖前面安装的内容。

基于本文碰到的情况，在stackoverflow中有一个类似的问答。它比较好的解释了这种情况。
[https://stackoverflow.com/questions/63722558/different-python-packages-with-the-same-top-level-name](https://stackoverflow.com/questions/63722558/different-python-packages-with-the-same-top-level-name)

下面是原文回答：

By default python would recognise only one of your two packages with one overwriting the other in the session.

If you put the following line in both your init.py files in the mypkg packages, you merge the packages together.

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
What will happen is that instead of overwriting one package with another python puts the content of the packages into the same mypkg namespace.

However be warned, clashing modules or sub packages are not resolved automatically.

So if you create a runner sub package in both mypkg packages only one of the runner packages will be loaded.