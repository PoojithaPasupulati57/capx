from flask import Flask,request,redirect,url_for,render_template,flash,jsonify,session
import requests
from otp import genotp
from cmail import sendmail
from token_1 import encode,decode
from flask_session import Session
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO 
import base64
import mysql.connector 
import os
os.chdir(os.path.abspath(os.curdir))
from mysql.connector import (connection)
mydb = connection.MySQLConnection(user='root',password='admin',host="localhost",database='capx')

#here
"""
os.chdir(os.path.abspath(os.curdir))
db=os.environ['RDS_DB_NAME']
user=os.environ['RDS_USERNAME']
password=os.environ['RDS_PASSWORD']
host=os.environ['RDS_HOSTNAME']
port=os.environ['RDS_PORT']
with mysql.connector.connect(host=host,user=user,password=password,db=db) as conn:
    cursor=conn.cursor(buffered=True)
    cursor.execute("CREATE TABLE if not exists users(u_id INT AUTO_INCREMENT PRIMARY KEY,  username VARCHAR(100) DEFAULT NULL,email VARCHAR(100) UNIQUE NOT NULL,password VARBINARY(10))")
    cursor.execute("CREATE TABLE if not exists stock(id INT AUTO_INCREMENT PRIMARY KEY,  stock_name VARCHAR(50) NOT NULL,quantity INT DEFAULT NULL,  ticker VARCHAR(50) NOT NULL,buy_price DECIMAL(10, 2) DEFAULT NULL, u_id INT,  FOREIGN KEY (u_id) REFERENCES users(u_id),UNIQUE KEY (u_id, ticker),  UNIQUE KEY unique_ticker_user (u_id, ticker), UNIQUE KEY unique_user_ticker (u_id, ticker))")
    cursor.execute("CREATE TABLE if not exists deleted_stocks (id INT AUTO_INCREMENT PRIMARY KEY, u_id INT,  FOREIGN KEY (u_id) REFERENCES users(u_id),ticker VARCHAR(10) NOT NULL,KEY u_id (u_id))")
    cursor.close()

mydb=mysql.connector.connect(host=host,user=user,password=password,db=db,pool_name='DED',pool_size=30)
#tooo
"""
app=Flask(__name__)
app.secret_key='code@12'
app.config['SESSION_TYPE']='filesystem'
Session(app)
api_key='your_key'
l=[]
l1=set()
@app.route('/')
def protfolio():
    return render_template('index.html')
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=='POST':
        susername=request.form['username']
        semail=request.form['email']
        spassword=request.form['password']
        cpassword=request.form['cpassword']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where email=%s',[semail])
        var1=cursor.fetchone()
        print(var1)
        if var1[0]==0:
            sotp=genotp()
            udata={'username':susername,'useremail':semail,'password':spassword,'otp':sotp}
            print(udata['otp'])
            subject='otp for Simple Portfolio Tracker'
            body=f'verify email by using the otp {sotp}'
            sendmail(to=semail,subject=subject,body=body)
            flash('OTP has sent to your Email')
            return redirect(url_for('otp',gotp=encode(data=udata)))
        elif var1[0]==1:
            flash('Email already existsed')
            return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/otp/<gotp>',methods=['GET','POST'])
def otp(gotp):
    if request.method=='POST':
        uotp=request.form['otp']
        try:
            dotp=decode(data=gotp)
        except Exception as e:
            print(e)
            flash('something went wrong')
            return redirect(url_for('create'))
        else:
            if uotp==dotp['otp']:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into users(username,email,password) values (%s,%s,%s)',[dotp['username'],dotp['useremail'],dotp['password']])
                mydb.commit()
                cursor.close()
                flash("login to ur account")
                return redirect(url_for('login'))
            else:
                flash('otp was wrong')
                return redirect(url_for('otp',gotp=gotp)) 
    return render_template('otp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        lusername=request.form['username']
        lemail=request.form['email']
        lpassword=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(email) from users where email=%s',[lemail])
        bdata=cursor.fetchone()
        if bdata[0]==1:
            cursor.execute('select password from users where email=%s',[lemail])
            bpassword=cursor.fetchone()
            if lpassword==bpassword[0].decode('utf-8'):
                session['user']=lemail
                return redirect(url_for('dashboard'))
            else:
                flash('password was wrong')
                return redirect(url_for('login'))
        else:
            flash('Email not registered pls register')
            return redirect(url_for('create'))    
    return render_template('login.html')
@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=='POST':
        stockname=request.form['stockname']
        ticker=request.form['ticker']
        quantity=request.form['quantity']
        buyprice=request.form['buyprice']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select u_id from users where email=%s',[session.get('user')])
        uid=cursor.fetchone()
        if uid:
            try:
                cursor.execute('insert into stock(stock_name,quantity,ticker,buy_price,u_id) values(%s,%s,%s,%s,%s)',
                               [stockname.upper(),quantity,ticker.upper(),buyprice,uid[0]])
                mydb.commit()
                cursor.close()
            except Exception as e:
                print(e) 
                flash('Data already exsits')
                return redirect(url_for('dashboard'))   

            else:
                flash('data added successfully')    
                return redirect(url_for('dashboard'))
        else:
            return 'something went wrong'    
    return render_template('Add.html')    
@app.route('/table')
def table():
    try:
        stock_data1 = ["aapl", "msft", "googl", "amzn", "tsla"]

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT u_id FROM users WHERE email = %s', [session.get('user')])
        uid = cursor.fetchone()

        if not uid:
            flash("User not found in session.")
            return render_template('stocktable.html')

        uid = uid[0]  

        cursor.execute('SELECT ticker FROM stock WHERE u_id = %s', [uid])
        existing_tickers = set(row[0] for row in cursor.fetchall())


        cursor.execute('SELECT ticker FROM deleted_stocks WHERE u_id = %s', [uid])
        deleted_tickers = set(row[0] for row in cursor.fetchall())


        for ticker in stock_data1:
            stock_name, price = None, None

            if ticker == "aapl":
                stock_name, price = "APPLE", 250
            elif ticker == "msft":
                stock_name, price = "MICROSOFT", 400
            elif ticker == "googl":
                stock_name, price = "GOOGLE", 180
            elif ticker == "amzn":
                stock_name, price = "AMAZON", 220
            elif ticker == "tsla":
                stock_name, price = "TESLA", 400

            if stock_name and ticker.upper() not in existing_tickers and ticker.upper() not in deleted_tickers:
                try:
                    cursor.execute(
                        'INSERT INTO stock (stock_name, quantity, ticker, buy_price, u_id) VALUES (%s, %s, %s, %s, %s)',
                        [stock_name, 1, ticker.upper(), price, uid]
                    )
                    mydb.commit()
                except Exception as e:
                    mydb.rollback() 
                    print(f"Error inserting stock {stock_name}: {e}")
                    flash(f"Could not add {stock_name}. Please try again.")
            else:
                print(f"Stock {stock_name} already exists for user.")

        cursor.execute(
            'SELECT id, stock_name, quantity, ticker, buy_price FROM stock WHERE u_id = %s',
            [uid]
        )
        notesdata = cursor.fetchall()
        cursor.execute('select ticker from stock where u_id=%s',[uid])
        s_data=cursor.fetchall()
        print(s_data)
        return render_template('stocktable.html', notesdata=notesdata)

    except Exception as e:
        print(f"Error in /table route: {e}")
        return render_template('stocktable.html')
    finally:
        cursor.close()  
@app.route('/stockdata',methods=['GET','POST'])
def stock_data():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select u_id from users where email=%s',[session.get('user')]) 
    uid=cursor.fetchone()
    cursor.execute('select ticker from stock where u_id=%s',[uid[0]])
    s_data=cursor.fetchall()
    l1=set()
    for i in range(len(s_data)):
        i1=s_data[i][0]
        l1.add(i1)
    prices={}    
    for i in l1:
        try:
            api_url=f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={i}&interval=1min&apikey={api_key}'
            a=requests.get(api_url).json()
            time=a.get("Time Series (1min)")
            s=a.get("Meta Data")
            if time:
                latest_time=next(iter(time))
                latest_price=time[latest_time]["1. open"]
                symbol=s["2. Symbol"]
                prices.update({symbol:latest_price})
            else:
                print("not planned")  
        except Exception as e:
            print(e)         
        else:
            print("ok")
    session['prices']=prices        

    return jsonify(prices) 
@app.route('/dashboard')
def dashboard():
    prices=session.get('prices',{})
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select u_id from users where email=%s',[session.get('user')]) 
    did=cursor.fetchone()
    cursor.execute('select quantity,ticker from stock where u_id=%s',[did[0]])
    d_data=cursor.fetchall()
    t=[]
    T=0
    d={}
    a_1=[]
    b_1=[]
    z={}
    print(prices)
    for i in range(len(d_data)):
        d.setdefault(d_data[i][1],d_data[i][0])
    if prices:
        for i in prices:
            if i in d:    
                p1=prices[i]
                p2=float(p1)
                p3=int(p2)
                d1=d[i]
                f=(p3*d1)
                z.update({i:f})
                t.append(f)
    else:
        prices={'AAPL': '243.3600', 'GOOGL': '191.9700', 'TSLA': '413.0692', 'MSFT': '424.5000',
                 'AMZN': '224.2500'}            
    T=sum(t)
    print(f'z is{z}')
    P=""
    PR=""
    for i in prices:
        if prices[i]>P:
            P=prices[i]
            PR=i  
    for i in z:
        c_1=z[i]
    
        c_3=(c_1/T)*100
        
        a_1.append(c_3)
        b_1.append(i)
    print(a_1)
    print(T)



    fig, ax = plt.subplots()
    plt.pie(a_1, labels=b_1, autopct="%0.1f%%", radius=1.5, textprops={"fontsize": 15})
    ax.axis('equal')
    plt.legend(loc=2)

   
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)


    chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    
    return render_template('Dashboard.html',prices=prices,T=T,PR=PR,chart_base64=chart_base64)  
@app.route('/update/<nid>',methods=['GET','POST'])
def update(nid):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from stock where id=%s', [nid])
    notesdata=cursor.fetchone()
    if request.method=='POST':
        stockname=request.form['stockname']
        ticker=request.form['ticker']
        quantity=request.form['quantity']
        buyprice=request.form['buyprice']
        try:
            cursor.execute('update stock set stock_name=%s , quantity=%s,ticker=%s,buy_price=%s where id=%s', [stockname,quantity,ticker,buyprice,nid])
            mydb.commit()
        except Exception as e:
            print(e)
            print("updte")    
        else:
            flash('notes updated successfully')
            return redirect(url_for('dashboard'))

    
    return render_template('update.html',notesdata=notesdata)  
@app.route('/delete/<nid>')
def delete(nid):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select u_id ,ticker from stock where id=%s',[nid])
        d_1=cursor.fetchone()
        print(d_1)
        cursor.execute('insert into deleted_stocks(u_id,ticker) values(%s,%s)',[d_1[0],d_1[1]])
        cursor.execute('delete from stock where id=%s',[nid])
        mydb.commit()
    except Exception as e:
        print(e)
        flash('notes not found')
        return redirect(url_for('dashboard'))
    else:
        flash('notes deleted successfully')
        return redirect(url_for('dashboard'))      
if __name__ == '__main__':
    app.run()      