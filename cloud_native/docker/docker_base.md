### Dockerfile
Dockerfile是用来构建docker image的文件。文件名一定要是Dockerfile。Dockerfile中有下面这些命令
- FROM (指定基础镜像)
- WORKDIR (指定当前目录)
- ENV (设置环境变量)
- ARG (设置环境变量，仅在Dockerfile内有效)
- VOLUME (挂载)
- RUN (运行命令)
- CMD (容器启动的时候运行的命令)


### Docker Command
- docker commit
- docker run
- docker start
- docker stop
- docker container ls/rm
- docker image ls/rm
- docker exec -it [container_name] /bin/bash
- docker network



### 经验
1、如何在Dockerfile中Copy父亲目录中的内容？
实现不了，但是可以直接在父亲目录中进行docker build，然后用-f 指定Dockerfile的路径。例如：<br>
docker build -t xx:0.0.1 -f ./folder/Dockerfile .

2、docker如何推送到远端hub？
docker push 可以实现推送，但是要注意的是本地的image名字和远端路径要一致才行，比如你的dockerid是shopper，那么本地的image需要是shopeer/xxx:0.0.1这样子的格式。

3、docker build --build-arg key=value .  这样构建的时候，key在Dockerfile中要用ARG key申明一下才能起作用(ENV声明不起作用)。

4、Dockerfile中最后一个CMD中的命令中环境变量需要用ENV设置，因为这一条命令是镜像打好后进入容器的时候运行的。

5、Dockerfile中的ARG和ENV的区别？
ARG是仅仅在Dockerfile中有效的环境变量，它搭配--build-arg来起作用。而且--build-arg后面跟的变量一定要在Dockerfile中用ARG定义过才起作用。
ENV则是定义了container中的变量，这个可以搭配docker run -e key=value来起作用，但用-e指定环境变量的时候，并不一定需要Dockerfile用ENV定义。