# 部署前端网页

## 安装 nodejs

> 本过程不需要在服务器上进行，建议在本机构建好静态资源后直接上传到服务器。Windows 下有 nodejs 的安装包，安装较为方便。下面演示的安装过程是 Linux 
> 操作系统上的安装方法。

使用包管理工具或 nvm 安装 nodejs，这里以 nvm 为例，nvm 是一个 nodejs 的版本管理工具，使用 nvm 可以方便的下载任意版本的 nodejs。

首先安装 nvm：

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
```

安装 nodejs 的 LTS 版本：

```sh
nvm install --lts
nvm use --lts
```

测试是否安装成功：

```sh
node --version
npm --version
```

## 构建静态资源

克隆前端代码：

```sh
git clone https://github.com/Statuey/plant.git
```

安装依赖（如果遇到网络问题请使用 npm 镜像来下载）：

```sh
cd plant
npm install
```

构建静态资源：

```sh
npm run build
```

构建好的文件存储在 `dist` 目录下。

## 上传到服务器

构建好的静态资源建议存放在服务器的 `/var/www/plant` 位置。可以使用 `scp` 或 `rsync` 工具将资源上传到服务器。
