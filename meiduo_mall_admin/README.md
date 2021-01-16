# meiduo_mall后台管理站点前端工程

> A Vue.js project

一下任选其一运行后台管理站点的前端服务。

### 一、第一种方式(端口号固定8081)

##### 1、安装依赖

```shell
# install dependencies
npm install
```

##### 2、编译出静态文件(编译好的静态文件存储在dist目录)

```shell
# build for production with minification
npm run build
```

##### 3、运行开发服务器

``` bash
cd meiduo_mall_admin
# serve with hot reload at localhost:8080
npm run dev
```

### 二、第二种运行方式

```shell
cd meiduo_mall_admin/dist
python3 -m http.server 8081
```

