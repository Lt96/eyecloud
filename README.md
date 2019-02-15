# eyecloud
#安装redis
https://www.cnblogs.com/zuidongfeng/p/8032505.html
#报错 is running/crashed   直接删除了pid文件


#安装py3    https://www.cnblogs.com/kimyeee/p/7250560.html
#zipimport.ZipImportError: can't decompress data   solution：https://blog.csdn.net/u014749862/article/details/54430022/


#Cache entry deserialization failed, entry ignored   未解决

#celery问题
1. 大小写
2. export C_FORCE_ROOT="True"  #ROOT启动



#修改commit 以及安装celery
 1130  vim routes/commit.py 
 1138  python3 -m pip celery=3.1.24
 1139  python3 -m pip install celery=3.1.24
 1140  python3 -m pip install celery==3.1.24
 1141  python3 -m pip install -U pip
 1142  python3 -m pip install celery==3.1.24

#python3 -m pip install          与      pip3 isntall 有区别

#检查注释的部分

#算法服务器防火墙开启5000端口，物理机开启33333端口 （记得重启防火墙）

#修改数据库连接方式换成物理机:33333

#tornado。server添加listen adress=0.0.0.0

#算法.py import json

#后台运行
#export C_FORCE_ROOT="true"

#nohup celery worker -A tasks.celery_config -l info -c 2  1>/home/data/yuanz/celery/outputlog 2>/home/data/yuanz/celery/errlog &

#nohup python3 tornado_server.py --port=5000 --log_file_prefix=./logs/5000.log --log_rotate_mode=time --log_rotate_when=H #--log_rotate_interval=1  1>/home/data/yuanz/tornado/outputlog 2>/home/data/yuanz/tornado/errlog &
