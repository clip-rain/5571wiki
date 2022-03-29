### Dockerfile
Dockerfile是用来构建docker image的文件。文件名一定要是Dockerfile。Dockerfile中有下面这些命令
- FROM (指定基础镜像)
- WORKIR (指定当前目录)
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