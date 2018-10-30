from datetime import datetime
import pymysql
from time import sleep
from emailsending1 import send_email
from error_update import updating_db




#db = pymysql.connect(host="localhost",user="root",password="root",db = "dashboard")
#c = db.cursor()
#c.execute("""select TaskMasterId ,DelayGracePeriodInSec from SubTaskMaster """)
#gd = c.fetchall()
#c.close()
#db.close()
#gd= {"j"+str(k):v for k,v in list(gd)}
#print("data.....",gd)



time = datetime.now()
time = time.strftime("%Y-%m-%d")
print(time)




def job_start_checking(job,date):
    db = pymysql.connect(host="localhost",user="root",password="root",db = "dashboard")
    c = db.cursor()
    c.execute("""select TaskName ,Time(StartTime) as start_time,ActualStartTime,StepName from TaskExecutionTracker 
              JOIN SubTaskMaster ON SubTaskMaster.bTaskMasterId = TaskExecutionTracker.SubTaskMasterId
              JOIN TaskMaster ON SubTaskMaster.TaskMasterId = TaskMaster.skMasterId
              WHERE StartTime >= '{0}' and StartTime != '' """.format(str(date+ " "+"00:00:00.000000")))
    d = c.fetchall()
    c.close()
    db.close()

    #d =["j"+str(k)+" "+str(s) for k,v,m,s in d]
    d =[str(k)+"-"+str(s) for k,v,m,s in d]
    n=[]
    d= ['CalculateDailyBalanceInterest_MST-90 Days Interest Cap', 
        'CalculateDailyBalanceInterest_MST-CalculateDailyBalanceInterest', 
        'CalculateDailyBalanceInterest_MST-GenerateLOCStatementJob', 
        'CalculateDailyBalanceInterest_MST-Delinquent Job']
    for i in d:
          if i not in n:
            n.append(i)
    print("started jobs...",n)
    return [x for x in job if x not in n]
        
def job_starting():
    time1 = datetime.now()
    #date = time1.strftime("%Y:%m:%d")
    time1 = time1.strftime("%H:%M")
    
    time1 ="1:30"
    #print(time1)
    db = pymysql.connect(host ="localhost",user="root",password ="root",db ="dashboard")
    c = db.cursor()
    c.execute("""select TaskName,ActualStartTime,StepName,skMasterId from SubTaskMaster JOIN TaskMaster ON SubTaskMaster.TaskMasterId = TaskMaster.skMasterId""" )
    d = c.fetchall()
    c.close()
    db.close()
    
    dic = {k:time+" "+str(v) for k,v,m,b in d}
    
    
    sub ={k:b for k,v,m,b in d}
    print("dic...........",sub)
    
    
    
    #d =["j"+str(k)+" "+str(m)+" "+str(v)[:4] for k,v,m in d]
    d =[str(k)+"-"+str(m)+" "+str(v)[:4] for k,v,m,b in d]
    n=[]
    for i in d:
          if i not in n:
            n.append(i)
    new_s = []
    print("jobs timings..",n)
    for i in n:
        if time1 in i:
            new_s.append(i[:-5])
    print("task needs to be started")
    print(new_s)
    print("checking for 1st time")
    a = job_start_checking(new_s,"2018-10-23")
    if  not a:
        print("true")
    else:
        print("jobs not started..",a)
        body= ",".join(a)
        #sleep(5)
        print("check again")
        a = job_start_checking(new_s,"2018-10-23")
        if a:
            #sleep(5)
            print("email...")
            send_email('saishanmukhgarugu@gmail.com','NTkxMTMzMjMz','garugusaishanmukh@gmail.com',"Jobs not yet started",body)
            d = body.split(",")
            print(d)
            for p in d:
                print(updating_db(str(sub[str(p.split("-")[0])]),str(p.split("-")[0]),str(p.split("-")[1]),str(dic[p.split("-")[0]]),str(1)))
            
            
#            a = job_start_checking(new_s,"2018-10-23")
#            print("jobs not started..",a)
#            if a:
#                sleep(5)
#                print("message")
#                print("jobs not started..",a)
#                
                
h = job_starting()
#g= job_start_checking("1:30")