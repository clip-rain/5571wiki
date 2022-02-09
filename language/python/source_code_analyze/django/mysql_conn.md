## 一、Django ORM
Django自带ORM组件。通过Django的ORM可以很方便地进行数据库操作。Django的ORM包是django.db。文本将从数据库的连接管理、SQL编译、延迟加载等方面研究一下Django ORM。


## 二、数据库连接管理
Django ORM支持包括mysql，oracle，postgresql，sqlite等多种数据库。下面以项目中用到的一种连接管理来探讨mysql的连接管理。

### 2.1 相关的依赖包
涉及到的包：
- django.db （django orm，默认依赖MySQLdb实现数据库连接）
- django.mysqlpool（类似于粘合剂的作用，将pymysql和sqlalchemy粘合起来，实现mysql连接的池化管理）
- pymysql （连接器，用于管理mysql连接）
- sqlalchemy （连接池管理）

### 2.2 django.db解读
#### 2.2.1 概览
下图是django.db包的大概结构。可以看到db下有backends和models两个子module。backends中包含了django支持的所有数据库。而models中则包含的是SQL解析相关内容。这里主要讨论的连接相关的内容都集中在backends中。
![](../../../../static/django.db.png)
下图是backends中的__init__.py文件中定义的BaseDatabaseWrapper，这是数据库包装类的基础类。每个数据库对应的包装类都会继承自这个基础类。
![](../../../../static/django.db.basedatabasewrapper.png)

#### 2.2.2 数据库管理
django/db/_\_init__.py中定义了一个全局变量connections，如下所示。connections这个全局的变量是用来管理多个数据库的。在使用上，大可以将connections看作是一个DatabaseWrapper数组来对待（这是因为ConnectionHandler实现了一些魔法方法）。
``` python
connections = ConnectionHandler()
```
在django/db/utils.py中有ConnectionHandler的详细定义。可以看到self._databases的定义来自于settings.DATABASES。

``` python
class ConnectionHandler(object):
    def __init__(self, databases=None):
        """
        databases is an optional dictionary of database definitions (structured
        like settings.DATABASES).
        """
        self._databases = databases
        self._connections = local()

    @cached_property
    def databases(self):
        if self._databases is None:
            self._databases = settings.DATABASES
        if self._databases == {}:
            self._databases = {
                DEFAULT_DB_ALIAS: {
                    'ENGINE': 'django.db.backends.dummy',
                },
            }
        if DEFAULT_DB_ALIAS not in self._databases:
            raise ImproperlyConfigured("You must define a '%s' database" % DEFAULT_DB_ALIAS)
        return self._databases

    def __getitem__(self, alias):
        if hasattr(self._connections, alias):
            return getattr(self._connections, alias)

        self.ensure_defaults(alias)
        db = self.databases[alias]
        backend = load_backend(db['ENGINE'])
        conn = backend.DatabaseWrapper(db, alias)
        setattr(self._connections, alias, conn)
        return conn

    def __iter__(self):
        return iter(self.databases)

    def all(self):
        return [self[alias] for alias in self]
```
这里的settings.DATABASES就是业务代码中设置的DATABASES。如下所示，它本质是一个存有数据库连接信息的字典。
``` python
{
    'abc_db':  {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django_mysqlpool.backends.mysqlpool',
        'NAME': 'abc_db',
        'HOST': 127.0.0.1,
        'PORT': 3306,
        'USER': root,
        'PASSWORD': 123456,
        'CONN_MAX_AGE': 3600,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```
另外ConnectionHandler.all()是非常重要的一个方法。她会遍历self.\_databases, 这里每个遍历的变量名为alias。之后self[alias]会自动调用魔法方法__getitem__，这个方法会根据alias中的数据库连接信息，生成对应的DatabaseWrapper。特别注意的是下面三句。从alias中获取‘ENGINE’，也就是对应的数据库类路径。由上面贴出来的配置可知，ENGINE配置的是django_mysqlpool.backends.mysqlpool。后面将连接管理的部分会详细讲解这块。
``` python
db = self.databases[alias]
backend = load_backend(db['ENGINE'])
conn = backend.DatabaseWrapper(db, alias)
```
综上，得出下面两点重要结论
- 可以认为全局变量connections是数据库管理的核心，若把它看作一个list，它里面是可以同时存放不同类型的数据库对象。例如,<br>
 [Mysql_DB1, Mysql_DB2, PostgreSQL_DB1, Oracle_DB1]<br>
- ConnectionHandler获取database信息是django orm和业务代码的一个交点。光说使用django orm的话，知道了这一点就足够了。

#### 2.2.3 连接池管理
在2.2.2小节中提供的数据库连接信息中可以看到，DATABASE中的ENGINE配置的是[django_mysqlpool.backends.mysqlpool](https://pypi.org/project/django-mysqlpool/#description)。而实际上django自带的bankends并没有mysqlpool。它是一个由smartfile公司开发的扩展包。这里之所以称之为扩展包，是因为mysqlpool是通过moneky-patch django mysql backend的方式工作的。也就是说，实际的的连接管理还是由django mysql backend来实现的。mysqlpool只是多做了一部分连接池化的工作。<br>
下面是mysqlpool的部分代码。其实mysqlpool整个包就一个base.py文件，总代码量不足100行，那它是如何实现池化的呢？看下面代码中的MYSQLPOOL定义，它是通过调用pool.manage得到的。也就是说真正的pool定义以及pool的实现都是在[sqlalchemy](https://www.sqlalchemy.org/)之中。<br>
那sqlalchemy又是什么东西呢？它其实是一个python工具包+ORM组合体。实际上仅仅用sqlalchemy的功能也可以实现数据库的增删改查功能，廖雪峰网站上有[教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1017803857459008)。

```python
import sqlalchemy.pool as pool

# Define this here so Django can import it.
DatabaseWrapper = base.DatabaseWrapper

# Wrap the old connect() function so our pool can call it.
OldDatabase = OldDatabaseProxy(base.Database.connect)


def get_pool():
    "Creates one and only one pool using the configured settings."
    global MYSQLPOOL
    if MYSQLPOOL is None:
        backend = getattr(settings, 'MYSQLPOOL_BACKEND', MYSQLPOOL_BACKEND)
        backend = getattr(pool, backend)
        kwargs = getattr(settings, 'MYSQLPOOL_ARGUMENTS', {})
        kwargs.setdefault('poolclass', backend)
        # The user can override this, but set it by default for safety.
        kwargs.setdefault('recycle', MYSQLPOOL_TIMEOUT)
        MYSQLPOOL = pool.manage(OldDatabase, **kwargs)
        setattr(MYSQLPOOL, '_pid', os.getpid())
    if getattr(MYSQLPOOL, '_pid', None) != os.getpid():
        pool.clear_managers()
    return MYSQLPOOL


def connect(**kwargs):
    "Obtains a database connection from the connection pool."
    conv = kwargs.pop('conv', None)
    if conv:
        # SQLAlchemy serializes the parameters to keep unique connection parameter
        # groups in their own pool. We need to store conv in a manner that is
        # compatible with their serialization.
        kwargs['conv'] = HashableDict(conv)
    # Open the connection via the pool.
    return get_pool().connect(**kwargs)


# Monkey-patch the regular mysql backend to use our hacked-up connect() function.
base.Database.connect = connect

```

#### 2.2.4 连接管理

