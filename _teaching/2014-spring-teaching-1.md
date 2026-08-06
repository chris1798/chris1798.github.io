---
title: "Docker 環境變數no_proxy注入"
collection: teaching
type: "Docker"
permalink: /teaching/2026-08-06-docker-1
venue: "University 1, Department"
date: 2026-08-06
location: "City, Country"
---

使用 env_file
======
將環境變數寫在單獨檔案，例如 app.env：

app.env內容：
======
no_proxy=localhost,127.0.0.1,172.18.xx.xx

docker-compose.yml 中透過 env_file 引用：
======
version: '3'

services:
  app:
    image: your_image_name
    env_file:
      - app.env

重啟docker container
======
docker compose up -d
