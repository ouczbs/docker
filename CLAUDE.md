发v从 从v# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个多容器 Docker 项目，用于部署本地开发环境。项目包含多个服务，通过 docker-compose 进行编排。

## 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 启动指定服务
docker-compose up -d jupyter

# 重新构建镜像
docker-compose build

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f nginx

# 停止所有服务
docker-compose down

# 查看服务状态
docker-compose ps
```

## 服务架构

- **nginx**: 反向代理服务 (端口 27443, 27001)
- **jupyter**: Jupyter Notebook 服务 (端口 8888)
- **anki**: Anki 同步服务器 (端口 27701)
- **gitea**: Git 服务 (端口 3000, 222)
- **db**: MySQL 数据库 (无外部端口)
- **miniconda**: Miniconda 环境 (端口 9999)
- **ssh**: SSH 服务

所有服务连接在 `nginx` 网络中。

## 数据卷

- `/data/anki`: Anki 数据
- `/data/gitea`: Gitea 数据
- `/data/mysql`: MySQL 数据
- `/root/docker`: Jupyter 数据

## 配置文件

- `docker-compose.yml`: 主配置文件，定义所有服务
- `nginx/nginx.conf`: Nginx 主配置
- `nginx/conf.d/`: Nginx 子配置目录