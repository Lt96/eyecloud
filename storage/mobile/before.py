import pymysql

class pyc:
    def pytomy(self,taskid,reportid,name,funduspath,status, rep):
        # 数据库连接

        rep=int
        taskid = str(taskid)
        reportid=str(reportid)
        name = str(name)
        funduspath = str(funduspath)
        status = str(status)




        con = pymysql.connect(host='10.20.71.67', port=33333, user='root', db='storage', passwd='qq714142541')
        mycur = con.cursor()

        # insert into jsontest(reportid,status,genre) values("DEMO-00011", "0", "1" )
        sql1 = "insert into test(taskid,reportid,name,funduspath,status) " \
               "values(" + '"' + taskid + '"' + ", " '"' + reportid + '"' + ", "  '"' + name + '"' + ", " + '"' + funduspath + '"' + ", "+ '"' + status + '"' + ", " " )"

        sql2 = "SELECT * FROM test \
                           WHERE taskid=" + '"' + taskid + '"'

        print(sql2)

        mycur.execute(sql2)
        res = mycur.fetchall()

        if res == ():
            rep=1
            mycur.execute(sql1)
            mycur.connection.commit()
            return rep

        else:
            rep=0

            return rep

        con.close()
