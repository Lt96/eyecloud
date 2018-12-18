# eyecloud
#安装redis
https://www.cnblogs.com/zuidongfeng/p/8032505.html
#报错 is running/crashed   直接删除了pid文件


#安装py3    https://www.cnblogs.com/kimyeee/p/7250560.html


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
