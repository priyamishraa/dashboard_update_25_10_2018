import emailsending1
import sqlite3
from flask import jsonify
import flask

def fetching():
    try:
        conn = sqlite3.connect('/home/administrator/sqdata.db')
        c = conn.cursor()
        c.execute("""SELECT time,error FROM stuffToPlot""")
        row = list(c.fetchall())
        #print(row)
        return list(row[-1])
        
    except:
        print("error")
 
    finally:
        c.close()
        conn.close()
        
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/app', methods=['POST'])
def home():
    print("checking...")
    data = fetching()
    print(data)
    if(data[1] == 'error occured'):
        emailsending1.send_email('saishanmukhgarugu@gmail.com','NTkxMTMzMjMz','garugusaishanmukh@gmail.com','text','hello')
        print
        return jsonify("email sent")
    else:
        return jsonify("email not sent")
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000')