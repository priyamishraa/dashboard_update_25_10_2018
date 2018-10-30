from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from support_functions import get_details,get_date_range
from datetime import datetime,timedelta

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



@app.route('/jobs_today', methods=['GET','POST'])
def jobs():
    if(request.method == 'POST'):
        date1 =datetime.now()
        date = get_date_range(date1.strftime("%Y-%m-%d"))
        p = request.form["filter"]
        print(p)
        d = get_details(date[1],[23,59,59],date[0],[23,59,59],"order by {0} ASC".format(p),str("job"))
        a = get_details(date[1],[23,59,59],date[0],[23,59,59],"order by {0} ASC".format(p),str("action"))
        c = {**d,**a}
        print(c)
        return(jsonify(d))
        
        
@app.route('/date_range', methods=['GET','POST'])
def date_range():
    if request.method =='POST':
        date1 = request.form["From"]
        date2 = request.form["To"]
        date1=datetime.strptime(date1, "%Y-%m-%d")
        date2 =datetime.strptime(date2, "%Y-%m-%d")
        return(jsonify(get_details(date1,[00,00,00],date2,[23,59,59],"order by StartTime ASC",str("job"))))

@app.route('/error_jobs', methods=['GET','POST'])
def error_jobs():
    date = get_date_range("2018-04-18")
    return(jsonify(get_details(date[1],[23,59,59],date[0],[23,59,59],"and TaskExecutionTracker.Status =0")))
        
if __name__ == "__main__":
    app.run(port =5003)