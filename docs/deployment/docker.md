# 安装 Docker

首先需要下载 Docker，不同的 Linux 发行版安装方法如下。

## 在 CentOS 上安装 Docker

首先卸载旧版本的 Docker：

```sh
sudo yum remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-engine
```

安装 `yum-utils` 包（提供 `yum-config-manager` 程序）并设置**稳定版本**的 repository。

```sh
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

安装最新版本的 Docker Engine 和 containerd：

```sh
sudo yum install docker-ce docker-ce-cli containerd.io
```


## 在 Ubuntu 上安装 Docker

首先卸载旧版本的 Docker：

```sh
sudo apt-get remove docker docker-engine docker.io containerd runc
```

更新 apt 包索引并安装包以允许 apt 通过 HTTPS 使用存储库：

```sh
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

添加 Docker 官方的 GPG 密钥：

```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

使用以下命令设置稳定版本存储库。

=== "x86_64 / amd64"

    ```sh
    echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

=== "armhf"

    ```sh
    echo \
    "deb [arch=armhf signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

=== "arm64"

    ```sh
    echo \
    "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

安装最新版本的 Docker Engine 和 containerd：

```sh
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

## 安装 docker-compose

下载编译好的 docker-compose 镜像：

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

建立软链接：

```sh
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

测试是否安装成功：

```sh
docker-compose --version
docker-compose version 1.29.2, build 1110ad01
```
