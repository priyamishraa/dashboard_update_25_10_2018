import pymysql
import flask
from flask import jsonify

#import emailsending1
from datetime import datetime,timedelta

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def fetching():
    
    try:
        time = datetime.now()
        time = time.strftime("%Y-%m-%d")
        print(time)
        db = pymysql.connect(host ="localhost",user="root",password ="root",db ="dashboard")
        c = db.cursor()
        c.execute("""SELECT skExecutionTrackerId,TaskName,SubTaskMasterId,StepName,
ActualStartTime,TIME(StartTime) as Start_time,TIME(EndTime) as End_time,
DelayGracePeriodINSec,TIMEDIFF(TIME(StartTime),ActualStartTime) as time_diff_starting,
EmailTriggerTimeInSec,
TaskExecutionTracker.Status,ErrorAction,DelayAction
                  FROM TaskExecutionTracker 
                  JOIN SubTaskMaster ON SubTaskMaster.bTaskMasterId = TaskExecutionTracker.SubTaskMasterId
                  JOIN TaskMaster ON TaskMaster.skMasterId = SubTaskMaster.TaskMasterId
                  WHERE StartTime >= '{0}' and StartTime != '' 
                  """.format(str(time+" 00:00:00.000000")))
        
        tasktracker = c.fetchall()
        print(tasktracker)
        return tasktracker
    
    except:
        print("error")

    finally:
        c.close()
        db.close()


def getSec_to_timeFormat(sec):
    time_format= str(timedelta(seconds=sec))
    return time_format
        
def action(starting_diff,Email_trigger_time,delay_grace,main_task,sub_task) :
    delay_grace_con = getSec_to_timeFormat(delay_grace)
    print("starting diff: "+starting_diff)
    delay_grace_con = "00:01:45"
    
    #print("dealy_grace: "+delay_grace_con)
    if(starting_diff > delay_grace_con):
        print("actual greater")
    if(starting_diff >= str(getSec_to_timeFormat(75))):
        if(starting_diff >= str(getSec_to_timeFormat(150)) ):
            if(starting_diff >= str(getSec_to_timeFormat(300))):
                print("calling")
            print("sms sending")
        print("email sending")
        text = "The {0} is not yet started ".format(main_task)
        print(text)
        print("\n")
    return 0

def job_started():
    date =datetime.now()
    date = date.strftime(date)
    
   
    #preapre a list of jobs and their starting time
    #using time date function calculate the current time and check in the db 
    #if job is not running perform action regarding that job
     
@app.route('/jobs', methods=['GET','POST'])
def job_fecting():
    data_fetched = fetching()
    d = {}
    print(data_fetched)
    FMT = '%H:%M:%S'
    for x in data_fetched:
        print(x[0])
        starting_diff = str(x[8])
        Email_trigger_time = x[10]
        delay_grace = x[7]
        start_time = str(x[5])
        end_time = str(x[6]).split(".")
        actual_start_time = str(x[4])
        print("end: "+str(x[6]))
        
        if (start_time ==  "None" or x[10] is not None ) and end_time[0] != "None":
            print("start_time required")
            current_running_time = str(datetime.strptime(end_time[0], FMT) - datetime.strptime(start_time, FMT))
            start_time = datetime.now()
            start_time = start_time.strftime("%H:%M:%S")
            print("not_started: "+start_time)
            print("actual_start: "+str(x[4]))
            starting_diff = str(datetime.strptime(actual_start_time, FMT) - datetime.strptime(start_time, FMT))
            action(starting_diff,Email_trigger_time,delay_grace,str(x[1]),str(x[3]))
            a = {'MainTask':x[1],'SubtaskID' : x[2],'SubtaskName' : x[3],'StartTime' : str(x[5]),'Status' : x[12],'current_running_time' :current_running_time}
            d[x[0]] = a
            

        elif (start_time !=  "None" or x[10] is not None):
            #current_running_time = str(datetime.strptime(end_time[0], FMT) - datetime.strptime(start_time, FMT))
            action(starting_diff,Email_trigger_time,delay_grace,str(x[1]),str(x[3]))
            a = {'MainTask':x[1],'SubtaskID' : x[2],'SubtaskName' : x[3],'StartTime' : str(x[5]),'Status' : x[12],'current_running_time' :current_running_time }
            d[x[0]] = a

    return jsonify(d)

if __name__ == "__main__":
    app.run(port=5003) 