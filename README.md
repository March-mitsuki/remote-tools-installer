# tools-installer
帮助国内服务器安装需要连接外网的工具

不需要找半天镜像，只需要你的电脑能连上外网就可以使用

# Requirements
需要你的远程服务器上安装有 python3.7 以上的 python 版本并且能通过 python3 进行调用

# Quick start
```sh
# clone this repo
git clone 'xxx'

cd xxx

pip install fire

python bin.py install pyenv --ssh_key path/to/your/ssh/key --user root --host target_server_ip_or_host
```

# How it works
你在中转机器上运行这个脚本，这个中转机器要求既能访问外网又能访问你的目标服务器。
然后脚本会下载需要的文件和依赖到中转机器上然后通过ssh和scp等命令把文件打包上传到目标服务器后安装。
