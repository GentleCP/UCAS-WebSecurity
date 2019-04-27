# 我的个人网站
## 一、功能列表
- 博客文章展示
- 用户注册登录
- 用户评论

## 二、系统架构
MyWebSite  
|--blog  # 博客app  
|--comment  # 评论app  
|--history  # 历史信息app（暂未上线）  
|--media  # 媒体文件（上传/图片）  
&emsp;|--picture  
&emsp;|--upload  
|--MyWebSite  # 主目录  
|--read_static  # 阅读统计  
|--static  # 静态文件  
|--templates  # 模板页面  
|--user  # 用户app（暂未上线）  
data.json  # 数据库数据文件  
manage.py # 管理文件  
README.md  # 项目说明文档  
requirements.txt  # 依赖包索引文件  
timezone_posix.sql  # 时区数据库文件  

## 三、部署说明
- 1、在github上克隆项目到本地
- 2、创建新的虚拟环境，安装requirements中的依赖包
- 3、创建mysql数据库，数据库名mywebsite（确保数据库用户与settings中一致）
- 4、migrate命令创建数据库表结构，用loaddata命令将data.json数据导入数据库
- 5、在mysql环境中用source命令将timezone_posix.sql导入，添加时区信息。