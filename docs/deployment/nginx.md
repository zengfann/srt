# 使用 Nginx 进行反向代理

使用 nginx 服务器进行反向代理：

在 `/etc/nginx/conf.d` 中创建 plant.conf 配置文件，填写以下内容：

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name <填写你的域名>;
    root <静态资源位置(/var/www/plant)>;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /files/ {
        alias <代码库位置(/root/code/srt)>/data/server/upload;
    }

    location /api {
        rewrite /api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

刷新 nginx 服务：

```sh
nginx -s reload
```