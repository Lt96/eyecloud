# eyecloud
#安装redis
https://www.cnblogs.com/zuidongfeng/p/8032505.html
#报错 is running/crashed   直接删除了pid文件


#安装py3    https://www.cnblogs.com/kimyeee/p/7250560.html


#Cache entry deserialization failed, entry ignored   未解决

#celery问题
 celery worker -A tasks.celery_config -l info -c 2
 1074  ls
 1075  celery worker -A tasks.celery_config -l info -c 2
 1076  ls tasks
 1077  mv funduslmage.py fundusImage.py
 1078  mv tasks/funduslmage.py tasks/fundusImage.py
 1079  ls tasks
 1080  celery worker -A tasks.celery_config -l info -c 2
 1081  vim tasks/fundusImage.py
 1082  vim services/afterpro.py
 1083  celery worker -A tasks.celery_config -l info -c 2
 1084  vim services/afterpro.py
 1085  celery worker -A tasks.celery_config -l info -c 2
 1086  vim services/afterpro.py
 1087  celery worker -A tasks.celery_config -l info -c 2
 1088  ls
 1089  ls services
 1090  vim services/afterpro.py
 1091  celery worker -A tasks.celery_config -l info -c 2
 1092  pip3 install pymysql
 1093  pip3 install -U pip
 1094  celery worker -A tasks.celery_config -l info -c 2
 1095  vim tasks/fundusImage.py
 1096  vim tasks/surfaceImage.py
 1097  celery worker -A tasks.celery_config -l info -c 2
 1098  vim tasks/surfaceImage.py
 1099  celery worker -A tasks.celery_config -l info -c 2
 1100  export C_FORCE_ROOT="True"  #ROOT启动
 1101  celery worker -A tasks.celery_config -l info -c 2


#修改commit 以及安装celery
 1130  vim routes/commit.py 
 1138  python3 -m pip celery=3.1.24
 1139  python3 -m pip install celery=3.1.24
 1140  python3 -m pip install celery==3.1.24
 1141  python3 -m pip install -U pip
 1142  python3 -m pip install celery==3.1.24

#python3 -m pip install          与      pip3 isntall 有区别
