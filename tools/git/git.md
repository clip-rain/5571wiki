### Git 常用命令
git init [--bare] 初始化
git branch --all  查看分支
git swtich 切换分支
git checkout 旧版本中也可用于切换分支，不过最新的版本推荐用switch
git add
git commit
git stash
git rebase
git reset
git cherry-pick
git merge
git push
git fetch
git pull
git remote [-v]
git config


### Git 底层命令和原理
Git的核心是一个简单的键值对数据库。我们可以往Git仓库中插入任意类型的内容。通过唯一的键可以在任意时刻取回该内容。
https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Git-%E5%AF%B9%E8%B1%A1 这篇中文文章写的很好。


git cat-file -p/-t  
git hash-object -w （-w表示写入到git的objects中）
git update-index --add --cacheinfo 10644 xxx filename
--cacheinfo 表示从Git数据库中往index中添加
git write-tree  将index中的内容保存成tree(并不回清空index)
git read-tree --prefix=xx xxx， 读取某个tree到index中，可以指定这些内容的前缀
git commit-tree xxx -p xxx

以上这些命令对Git数据库起作用，并不一定体现在当前目录的变化。另外这些底层命令还需要其他的命令粘合才能实现上层命令的功能。



### Reference

- [1] [https://git-scm.com/book/en/v2](https://git-scm.com/book/en/v2)