import pymysql

def updating_db(i,n,s,a,ac):
    try:
        db = pymysql.connect(host="localhost",user="root",password="root",db = "dashboard")
        c = db.cursor()
        sql = """INSERT INTO `Action_tracker` (`Job_Id`,`Job_name`,`Sub_task_name`,`Actual_time_to_start`,`Action`) values ("{0}","{1}","{2}","{3}","{4}")""".format(i,n,s,a,ac)
        #print(sql)
        c.execute(sql)
        db.commit()
        return "db updated"
    except:
        print("error")
    finally:
        c.close()
        db.close()
        