import pymysql
from datetime import datetime,timedelta

class getdaterange():
    def __init__(self):
        self.date = ""
    
    def get_date_range(date1):
        #date1 = date1.strftime("%Y-%m-%d")
        date1 = datetime.strptime(date1, "%Y-%m-%d")
        date2 =  date1 - timedelta(days=1)
        return [date1,date2]


class getdetails():
    def __init__(self,order):
        self.order = order
        self.data = []
        
    def get_details(self,p1,value1,p2,value2):
        p1=p1.replace(hour=value1[0], minute=value1[1], second=value1[2])
        p2=p2.replace(hour=value2[0], minute=value2[1], second=value2[2])
        
        self.data = self.job_fetching_ascending(p1,p2)
        b = self.framing_data()
        #a = self.Action_fetching(p1,p2)
        #c = {**b,**a}
        return b
    
    def job_fetching_ascending(self,date1,date2):
        try:
            order = self.order
            db = pymysql.connect(host="localhost",user="root",password="root",db = "dashboard")
            cursor = db.cursor()
            sql ='''SELECT skExecutionTrackerId, SubTaskMasterId,StepNumber,StepName,TaskMasterID, TaskName, 
            StartTime,EndTime,TaskExecutionTracker.Status, ActualStartTime,
            TIMEDIFF(ActualStartTime,TIME(StartTime)) AS DelayTime,
            TIMEDIFF(TIME(EndTime),Time(StartTime)) AS TaskExecutionTime,
            EmailTriggerTimeInSec, `SubTaskMaster`.DelayAction,
            `SubTaskMaster`.ErrorAction FROM `TaskExecutionTracker`
            JOIN SubTaskMaster ON TaskExecutionTracker.SubTaskMasterId = SubTaskMaster.bTaskMasterId
            JOIN TaskMaster ON SubTaskMaster.TaskMasterId = TaskMaster.skMasterId 
                    WHERE StartTime >="{0}" and StartTime <"{1}" {2} '''.format(date1,date2,order)
            #print(sql)
            cursor.execute(sql)
            data_fetched= cursor.fetchall()
            return list(data_fetched)
        except:
            print("error")
        finally:
            cursor.close()
            db.close()   

    def framing_data(self):
        a = self.data
        d = {}
        b = 0
        if a:
            for row in self.data:
                value = {'SubTaskname' : str(row[3]),
                     'MainTask' : str(row[5]),
                     'Start_Date' : str(row[6]).split(".")[0],
                     'End_Date' : str(row[7]).split(".")[0],
                     'Status' : str(row[8]),
                     'DelayAction':str(row[13]),
                     'ErrorAction':str(row[14]),
                     'ActualStartTime':str(row[9])
                     }
                d[str(b)] = value
                b +=1
        #print(d)
        return d
        
    def Action_fetching(self,date1,date2):
        try:
            db = pymysql.connect(host="localhost",user="root",password="root",db = "dashboard")
            cursor = db.cursor()
            sql ='''SELECT * from Action_tracker
                    WHERE Actual_time_to_start >="{0}" and Actual_time_to_start <"{1}"  '''.format(date1,date2)
            print(sql)
            cursor.execute(sql)
            data_fetched= cursor.fetchall()
            d = {}
            b = 0
            for row in data_fetched:
                value = {
                     'MainTask' : str(row[1]),
                     'Start_Date' : str(row[3])+".000000",
                     'Sub_task_name' : str(row[2]),
                     'Action':str(row[4]),
                     'End_Date' : str(datetime.now()),
                     'ActualStartTime':str(row[3])+".000000",
                     'Status':str(row[4])
                     }
                d["a"+str(b)] = value
                b +=1
            return d
        except:
            print("error")
        finally:
            cursor.close()
            db.close()

#class adding_user(object):
#    def __init__(self, username, password, a):
#        self.username = username
#        self.password = password
#        self.a = a
#        
#    def addinguser(self):
#        name = self.username
#        pwd = self.password
#        access = self.a
#        try:
#            db = pymysql.connect(host ="localhost",user="root",password ="root",db ="dashboard")
#            c = db.cursor()
#            c.execute("""INSERT INTO `user_details` (`username`, `password`, `access`) VALUES ('{0}', '{1}', '{2}');""".format(name,pwd,access))
#            db.commit()
#        except:
#            print("error")
#        finally:
#            c.close()
#            db.close()
#
#class fetch(object):
#    def fetching():
#        try:
#            db = pymysql.connect(host ="localhost",user="root",password ="root",db ="dashboard")
#            c = db.cursor()
#            c.execute("""SELECT * from user_details """)
#            tasktracker = c.fetchall()
#            return tasktracker
#        except:
#            print("error")
#        finally:
#            c.close()
#            db.close()