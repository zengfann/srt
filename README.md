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
    flask run
    ```

    B:在PyCharm中直接新建启动配置即可

## 代码检查（`IMPORTANT`）

安装`pre-commit`：

```sh
pip install pre-commit
pre-commit install
```

每次提交代码pre-commit都会检查代码中的问题，例如变量命名，代码风格，多余的空格等。

## 开发准则

1. 使用`from xxx import yyy`而不是`import xxx`
2. 变量名使用下划线小写字母命名，类名使用大驼峰命名
3. 包名使用全小写命名不包含下划线
