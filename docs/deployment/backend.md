# 部署 API 服务器

## 使用 Docker 启动 API 服务

安装完 Docker 后首先克隆本项目：

```sh
git clone https://github.com/zengfann/srt.git
```

进入本项目首先创建文件上传目录以及数据库数据目录：

```sh
cd srt
mkdir -p data/server data/db data/server/upload
```

将训练好的 `69.pth` 模型文件拷贝到 `data/server/69.pth` 目录：
```sh
cp <模型位置> data/server/69.pth
```

启动服务：

```sh
docker-compose up -d
```

启动过程中会下载 mongodb 镜像并构建本项目的镜像，在构建过程中会使用 pip 下载若干依赖，时间可能较长。服务启动成功后会跑在8000端口上，请确保8000端口没有被占用。

