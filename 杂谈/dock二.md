### Docker file

docker build -f [path_of_dockerfile]，当Dockerfile中有COPY，且需要COPY Dockerfile上级目录的内容的时候，可以直接在上级目录docker build，通过-f指定Dockerfile路径


将MAC本机中的虚拟环境COPY到容器内，如果容器的基础镜像是linux，则会出现MAC上的可执行文件copy过去后，不能执行。所以没法直接把本机调试好的代码以及对应的依赖打包进容器后直接运行。


