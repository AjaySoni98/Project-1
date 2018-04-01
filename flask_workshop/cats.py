from flask import Flask,render_template
from flask import request,session, redirect,json
import MySQLdb,string
app = Flask(__name__)
mysql = MySQLdb.connect(host='localhost',user="root",password="24184075",db="project")

@app.route('/')
def rest():
 return render_template('rest.html')

@app.route('/home')
def hello_world():
    author = "Shetty"
    name = "You"
    return render_template('index.html', author=author, name=name)

@app.route('/signup', methods = ['POST'])
def signup():
    _name = request.form['name']
    _email = request.form['email']
    _password = request.form['psw']
    cursor = mysql.cursor()
    cursor.callproc('sp_createUser',(_name,_email,_password))
    data=cursor.fetchall()
    cursor.close() 
    if len(data) is 0 :
        mysql.commit()
        cursor = mysql.cursor()
        sql = "CREATE TABLE "+_name+" (`id` INT NOT NULL AUTO_INCREMENT,`type` VARCHAR(45) NULL,`topic` VARCHAR(45) NOT NULL,`description` VARCHAR(100) NULL,`date_time` DATETIME NOT NULL,PRIMARY KEY (`id`))"
        cursor.execute(sql)
        return render_template('rest.html')
    else:
        return json.dumps({'html':'Username Exists Try Again'})
   
@app.route('/login', methods = ['POST'])
def login():
    _email = request.form['_email_']
    _password = request.form['_psw_']
    cur1 = mysql.cursor()
    cur1.execute("Select user_name from users where user_email=%s and user_password=%s",(_email,_password))
    result=cur1.fetchone()
    session['result']=result
    return render_template("emails.html",result=result)

@app.route('/home1')    
def login_1():
    return render_template('login.html')
     
@app.route('/emails')
def login_2():
    result=session.get('result')
    return render_template('emails.html',result=result)

@app.route('/view')
def view():
    result=session.get('result')
    result1=session.get('result')
    result=str(result).replace(",","")
    result=str(result).replace("(","")
    result=str(result).replace(")","")
    result=str(result).replace("'","")
    print(result)
    cur1 = mysql.cursor()
    cur1.execute("Select * from " + result)
    data=cur1.fetchall()
    return render_template("view.html",data=data,result1=result1)

@app.route('/meeting')
def meeting():
    result1=session.get('result')
    return render_template('meeting.html',result1=result1)

@app.route('/event')
def event():
    result1=session.get('result')
    return render_template('event.html',result1=result1)

@app.route('/create', methods = ['POST'])
def create():
    _topic = request.form['topic']
    _description = request.form['description']
    _datetime= request.form['datetime']
    _datetime=str(_datetime).replace("T"," ")
    print(_datetime)
    result=session.get('result')
    result1=str(result).replace(",","")
    result1=str(result1).replace("(","")
    result1=str(result1).replace(")","")
    result1=str(result1).replace("'","")
    cursor = mysql.cursor()
    cursor.execute("Insert into "+result1+"(`type`, `topic`, `description`, `date_time`) VALUES ('meeting',%s,%s,%s)",(_topic,_description,_datetime))
    mysql.commit()
    return render_template('emails.html',result=result)

@app.route('/create_e', methods = ['POST'])
def create_e():
    _topic = request.form['topic']
    _description = request.form['description']
    _datetime= request.form['datetime']
    _datetime=str(_datetime).replace("T"," ")
    print(_datetime)
    result=session.get('result')
    result1=str(result).replace(",","")
    result1=str(result1).replace("(","")
    result1=str(result1).replace(")","")
    result1=str(result1).replace("'","")
    cursor = mysql.cursor()
    cursor.execute("Insert into "+result1+"(`type`, `topic`, `description`, `date_time`) VALUES ('event',%s,%s,%s)",(_topic,_description,_datetime))
    mysql.commit()
    return render_template('emails.html',result=result)
     
if __name__ == '__main__':
    app.secret_key = 'some secret key'
    app.run()