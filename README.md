<pre>
PROJECT NAME:"SIMPLE STOCK PROTFOLIO"

PROJECT DESCRIPTION: The CapX Project is a web application built using Flask, designed to manage and track stock data, handle user authentication, and send email notifications with OTP (One-Time Password) for secure user actions.

#STEPS TO RUN PROJECT LOCALLY

STEP1: **Repository Link**:
       git clone https://github.com/PoojithaPasupulati57/capx.git

STEP2:
1.After opening above Link.
2.Create a folder in your local system(ex:capx)
3.Copy the templates folder that contain in frontend and paste in capx folder.
4.copy all files that contain in backend folder and paste it line by line in capx folder(make sure to unpack the folders).

STEP3:
1.Open ur Mysql command line client.
2.create database name capx
3.download capx.sql from repository.
4.after download copy the file path.
5.paste in cmd as(ex: SOURCE C:/Users/DELL/Downloads/capx.sql;) slashes need to be in forward slashes and SOURCE need to be first and remove (double quotes)

STEP4:
1.Open capx folder and In the address bar of the File Explorer, type cmd and press Enter.
2.Type Code .(give space in between code and .)
3.open cmail.py edit email_user and email_password.
   i.In email_user->Paste your email_id where u can see(#email_user).
   ii.In email_password->open your manage your google account
                       ->make sure 2-step verification is on.
                       ->later open App passwords(type in search bar)
                       ->type "mail" near create a new app-specific password
                       ->after typing "mail".click on create button
                       ->copy the Your app password for your device(ex:Abcd efgh Ijkl mnop) and click on done.
                       ->now open cmail.py and paste ur password in email_paassword.
  iii.make sure you paste email_user and email_password in '' in single quotes.    
  iv.open app.py in line 14 when we are giving sql connection change password="your mysql password" and change database="your database name" where tables are stored.
  v.AT line 19 in app.py .generate your api_key in alpha vantage website and paste it.
  
STEP5:
1.After code .(which has done in step 4)
2.after that ->pip install virtualenv
3.create a name->virtualenv cap
4.Now activate virtualenv->.\cap\Scripts\activate.
5.install packages after activate.
      ->pip install flask
      ->pip install flask-session
      ->pip install requests
      ->pip install matplotlib
      ->pip install mysql-connector-python
6.please make sure capx holder should contain templates folder only do not craete folders as frontend,backend only templates folder and py files should appear line by line down of templates and packages u have created.   
6.now run the app by using-py app.py
7.copy the url and paste it.
8.later create ur account and login.
9.after login the dashboard looks empty except table .so click on stock table(because to insert data in stock table)
10.After viewing stock table.click on url and paste your baseurl and /stockdata(ex:http://127.0.0.1:5000/stockdata)-by using this we can generate data by api_url(alpha vantage) with limit 25 per day
11.after viewing stock data click on(<-) backward arrow and u will come back to dashboard and refresh it (so that dashboard generate current prices of stockdata,total value,protfolio distribution)
12.Now you can see the dashboard with updated.       

STEP6:
1.now you add or update or delete the record but after doing any operations.please make sure you call stockdata route(ex:http://127.0.0.1:5000/stockdata) after perform any operations such as add,delete,update etc.. and refersh dashboard to view total value etc..

STEP7:(Deployment Links)
FRONTEND:
       ->Base URL:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app
       ->Add.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/Add.html
       ->Dashboard.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/Dashboard.html
       ->login.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/login.html
       ->otp.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/otp.html
       ->signup.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/signup.html
       ->stocktable.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/stocktable.html
       ->update.html:https://frontend-5ijqf4o3r-poojithas-projects-2047ac8a.vercel.app/update.html
BACKEND:
</pre>

  

       
