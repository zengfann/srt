# 南京农业大学 SRT 项目

## 开发流程

1. 下载依赖：

    ```
    pip install -r requirements.txt
    ```

2. 下载数据库（MongoDB）

    [下载链接](https://docs.mongodb.com/master/tutorial/install-mongodb-on-windows/)

3. 在工程下新建`.env`文件：

    内容如下，`MONGODB_HOST`会被flask读取用于连接数据库，`JWT_SECRET`用于JWT加密 `UPLOAD_FOLDER`用于上传图片存储

    ```
    MONGODB_HOST=mongodb://127.0.0.1:27017/srt
    JWT_SECRET=04d63553-4db7-4017-b5fd-32870ad71158
    UPLOAD_FOLDER=upload
    ```

4. 启动开发服务器（A or B）

    A:在控制台下：

    ```sh
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run dev
    ```

    B:在PyCharm中直接新建启动配置即可

5. 创建模型测试文件夹 `model`文件夹(用于存储测试识别模型)
   需要在`ml`文件下修改`recognize.py` 中模型的路径
   `model = torch.load("path", map_location=torch.device("cpu"))`

## 代码检查（`IMPORTANT`）

安装`pre-commit`：

```sh
pip install pre-commit
pre-commit install
```

每次提交代码pre-commit都会检查代码中的问题，例如变量命名，代码风格，多余的空格等，如果编码存在问题将不能commit代码，修复代码中的问题后再次提交即可。

如果想在不commit代码的情况下检查代码中存在的问题运行以下命令：

```sh
pre-commit run --all-files
```
