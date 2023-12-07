#Bank App Integration Project with ML Solution using Flask in python
#Import necessary liabraries and modules
from flask import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import mysql.connector

    
#Establish a connection to the MySql Database
db = mysql.connector.connect(
host = "localhost",
user = "root",
password = "",
database = "banking"
)
mycursor = db.cursor()

 

#Create a Flask Web Application
app=Flask(__name__)

 
#Define a route for the main page(login)
#decorator- to build url pattern to specific function.
@app.route("/",methods=['GET','POST'])
def login():
    #Handle login form submission
    if request.method=="POST":
        #Retriver account number and password from the form
        Acc = int(request.form['AccountNumber'])
        Pwd = request.form['Password']
        print(Acc,Pwd)

        #Execute a SQL query to validate user credentials
        query = "SELECT * FROM `details` WHERE Account=(%s) and password=(%s)"
        values = (Acc,Pwd,)
        mycursor.execute(query,values)
        Records = mycursor.fetchall() 
        print(len(Records))

        #Check if login is successful and redirect to the dashboard or show an error
        if len(Records)==1 and int(Records[0][2])==Acc and Records[0][6]==Pwd:
            return dashboard()
        elif len(Records)>1 or len(Records)<1:
            return render_template("home.html", error="Invalid Details")
        else:
            return render_template("home.html", error="Invalid Details")
    else:
        return render_template("home.html", error="")

#Define a route for the dashboard
@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    return render_template("mainpage.html")

#Define a route for user registeration(Signup)
@app.route("/signup", methods=['GET','POST'])
def signup():
    #Handle Signup form Submission
    if request.method=="POST":
        #Retrive user Registeration data from the form
        Hname=request.form['Holdername'] 
        Ifsc=request.form['IFSCcode']
        Accno=request.form['Accountnumber']
        Bname=request.form['BankName']
        Brname=request.form['BranchName']
        Mblno=request.form['MobileNumber']
        password2=request.form['Password']
        cpwd=request.form['ConfirmPassword']
        signupdata = request.form
        #return render_template("home.html")

        #Validate password match and insert user data into database
        if(password2==cpwd):
            signupdata = request.form
            query2 = "INSERT INTO details SET name=(%s),IFSCcode=(%s),Account=(%s),Bname=(%s),Brname=(%s),mblnum=(%s),password=(%s)"
            values2 = (Hname,Ifsc,Accno,Bname,Brname,Mblno,password2,)
            print(values2)
            mycursor.execute(query2,values2)
            db.commit()
            return render_template("home.html", error='')
        else:
            return render_template("signup.html",error="Password mismatch", data=signupdata)
    else:
        return render_template("signup.html", error='', data='')

#Define a route for the main prediction page
@app.route("/mainpage",methods=['GET','POST'])
def mainpage():
    #Handle the main prediction form submission
    if request.method=="POST":
        #Retrive input data for the machine learning model
        #(Note: Ensure the form fields match the expected input features)
        age=request.form['age']
        job=request.form['job']
        marital=request.form['marital']
        edu=request.form['education']
        defa=request.form['default']
        house=request.form['housing']
        loan=request.form['loan']
        contact=request.form['contact']
        mon=request.form['month']
        day=request.form['day_of_week']
        dur=request.form['duration']
        cam=request.form['campaign']
        pred=request.form['pdays']
        prev=request.form['previous']
        pout=request.form['poutcome']
        emr=request.form['emp.var.rate']
        conp=request.form['cons.price.idx']
        conc=request.form['cons.conf.idx']
        eur=request.form['euribor3m']
        nemp=request.form['nr.employed']

        #Create a list with the input data
        data1=[]  
        # print(request.form)
        data1.append(request.form['age'])
        data1.append(request.form['job'])
        data1.append(request.form['marital'])
        data1.append(request.form['education'])
        data1.append(request.form['default'])
        data1.append(request.form['housing'])
        data1.append(request.form['loan'])
        data1.append(request.form['contact'])
        data1.append(request.form['month'])
        data1.append(request.form['day_of_week'])
        data1.append(request.form['duration'])
        data1.append(request.form['campaign'])
        data1.append(request.form['pdays'])
        data1.append(request.form['previous'])
        data1.append(request.form['poutcome'])
        data1.append(request.form['emp.var.rate'])
        data1.append(request.form['cons.price.idx'])
        data1.append(request.form['cons.conf.idx'])
        data1.append(request.form['euribor3m'])
        data1.append(request.form['nr.employed'])

        #Read the Pre-existing dataset preprocess it
        data=pd.read_csv(r'C:\Users\SATYA\Downloads\bank-additional\bank-additional.csv')
        #print(data.head())
        #print(data.shape)
        data=data.dropna()
        le=LabelEncoder()

        #Transform categorical features into numerical labels
        data['job']=le.fit_transform(data['job'])
        data['marital']=le.fit_transform(data['marital'])
        data['education']=le.fit_transform(data['education'])
        data['default']=le.fit_transform(data['default'])
        data['housing']=le.fit_transform(data['housing'])
        data['loan']=le.fit_transform(data['loan'])
        data['contact']=le.fit_transform(data['contact'])
        data['month']=le.fit_transform(data['month'])
        data['day_of_week']=le.fit_transform(data['day_of_week'])
        data['poutcome']=le.fit_transform(data['poutcome'])
        data=data.fillna(0)

        #Split the dataset into training and testing sets
        x=data.iloc[ : ,:-1].values
        y=data.iloc[:,-1].values
        xtrain,xtest,ytrain,ytest=train_test_split(x,y,random_state=8,test_size=0.2)

        #Create a Decision Tree model, train it, and make predictions
        model=DecisionTreeClassifier(criterion='entropy')#gini
        model.fit(xtrain,ytrain)
        ypred=model.predict(xtest)
        res1=accuracy_score(ytest,ypred)*100
        res=model.predict([data1])
        print(res1,res[0])

        #Render the result on the Prediction page
        return render_template("new.html",acc=res1,pre=res[0])

    #Render the main prediction page with empty results
    return render_template("mainpage.html", acc="",pre="")

#Run the flask application
if __name__=="__main__":
    app.run(debug=True)
