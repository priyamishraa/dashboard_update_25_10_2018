import pymysql

db = pymysql.connect(host ="localhost",user="root",password ="133233",db ="dashboard")
c = db.cursor()

c.execute("""SELECT skExecutionTrackerId,SubTaskMasterId,StartTime  FROM TaskExecutionTracker WHERE Status = 0""")
error_jobs = c.fetchall()
l=[]
d={}
#print(error_jobs)
for row in error_jobs:
        #print(row)
        if ('' not in list(row)):
            l.append(row)
            l = [x for x in l if x != ['']]
    #l=tuple(l)
for x in l:
        a = { 'SubTaskid' : x[1], 'StartTime' : x[2]}
        d[x[0]]=a
print(d)