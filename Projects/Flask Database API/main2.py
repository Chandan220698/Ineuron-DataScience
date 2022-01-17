from flask import Flask, render_template, request
import mysql.connector as connection
import csv
import pandas as pd
import pymongo

## Creating the client connecton (Because the passing of object clientConn between the different routes and html converting it to str)
def mongodbConn(clientURL):
    clientConn = pymongo.MongoClient(clientURL)
    return clientConn

# Function for sql connection
def mysql_basic(**kwargs):
    mydb = connection.connect(host=kwargs['host'], user=kwargs['user'], passwd=kwargs['passwd'], database = kwargs['database'], use_pure=True)
    print(mydb.is_connected())
    query = kwargs['query']
    cursor = mydb.cursor() #create a cursor to execute queries
    cursor.execute(query)

    if kwargs['commit'] == True:
        mydb.commit()


app = Flask(__name__) ## WSGP Application 

# Homepage
@app.route('/', methods = ['POST', 'GET'])    ## Decorator
def homepage():
    return render_template('homepage.html')

# Selection of database
@app.route('/dbConnection', methods = ['POST'])
def dbSelection():
    print(request.method)
    if request.method == 'POST':
        db_select = request.form['db']
        print(db_select)
        if db_select == 'mysql':
            return render_template('mysql.html', title = 'MySQL')
        elif db_select == 'mongodb':
             return render_template('mongoDB.html', title = 'MongoDB')

# MySQL - Select Operations
@app.route('/sqlCRUD', methods = ['POST'])
def mysqlCOnnection():
    try:
        host = request.form['host']
        user = request.form['user']
        passwd = request.form['passwd']
        mydb = connection.connect(host=host,user=user, passwd=passwd,use_pure=True)
        # check if the connection is established
        print('connection done')
        query = "SHOW DATABASES"
        cursor = mydb.cursor() #create a cursor to execute queries
        cursor.execute(query)
        db_list = cursor.fetchall()
        print(db_list)

    except Exception as e:
        mydb.close()
        print(str(e))

    return render_template('sql_curd.html', host=host, user=user, passwd=passwd, title = 'CURD', db_list=db_list, total_db=len(db_list))

# MySQL - Identify the Operation
@app.route('/sqlExecute/<host>/<user>/<passwd>', methods = ['POST'])
def sqlExecute(host, user, passwd):
    
    try:
        print("312312312")
        operation = request.form['operation']
        print(operation)
        if operation == 'create_table':
            return render_template('createTable.html', host=host, user=user, passwd=passwd, title = 'post')
        elif operation == 'insert_one':
            return render_template('insert_one.html', host=host, user=user, passwd=passwd, title = 'post')
        elif operation == 'insert_bulk':
             return render_template('insert_bulk.html', host=host, user=user, passwd=passwd, title = 'post')
        elif operation == 'update':
            return render_template('updateTable.html', host=host, user=user, passwd=passwd, title = 'post')
        elif operation == 'delete':
            return render_template('deleteTable.html', host=host, user=user, passwd=passwd, title = 'post')
        elif operation == 'download':
            return render_template('downloadTable.html', host=host, user=user, passwd=passwd, title = 'post')
    except Exception as e:
        print(str(e))

# MySQL - Create Table
@app.route('/createTable/<host>/<user>/<passwd>', methods = ['POST'])
def createTable(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    attr = request.form['attr']

    # Create Database if not exist then create table
    mydb = connection.connect(host="localhost", user="root", passwd="mysql",use_pure=True)
    # check if the connection is established
    print(mydb.is_connected())
    query = "CREATE DATABASE IF NOT EXISTS " + database
    cursor = mydb.cursor() #create a cursor to execute queries
    cursor.execute(query)

    query = "CREATE TABLE " + table + " ( " + attr + " )"
    mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit=False)
    #cursor = mydb.cursor() #create a cursor to execute queries
    #cursor.execute(query)
    print("Table Created!!")
    msg = "Table Create"

    return render_template('display.html', msg = msg)

# MySQL - Insert One
@app.route('/insertOne/<host>/<user>/<passwd>', methods = ['POST'])
def insertOne(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    data = request.form['data']

    query = "INSERT INTO " + database+"."+table + " VALUES ( " + data + " )"
    mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Data Inserted!!")
    msg = "Data inserted: [ {} ] | table: {} | DB: {}".format(data, table, database)

    return render_template('display.html', msg = msg)

# MySQL - Insert Bulk
@app.route('/insertBulk/<host>/<user>/<passwd>', methods = ['POST'])
def insertBulk(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    path = request.form['path']
    
    mydb = connection.connect(host=host, database=database, user=user, passwd=passwd, use_pure=True)
    cursor = mydb.cursor()  # create a cursor to execute queries
    with open(path, "r") as f:
        next(f)
        csv_data = csv.reader(f, delimiter="\n")
        for line in enumerate(csv_data):
            for list_ in (line[1]):
                cursor.execute('INSERT INTO {table} values ({values})'.format(values=(list_), table=table))
    print("Values inserted!!")
    mydb.commit()
    cursor.close()
    msg = "Bulk Data inserted: [ {} ] | table: {} | DB: {}".format(path, table, database)

    return render_template('display.html', msg = msg)

# MySQL - Update Table
@app.route('/updateTable/<host>/<user>/<passwd>', methods = ['POST'])
def updateTable(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    set = request.form['SET']
    where = request.form['WHERE']
    
    query = "UPDATE " + table + " SET " + set + " WHERE " + where
    print(query)
    mydb = connection.connect(host=host, database=database, user=user, passwd=passwd, use_pure=True)
    # check if the connection is established
    print(mydb.is_connected())
    cursor = mydb.cursor()  # create a cursor to execute queries
    cursor.execute(query)
    mydb.commit()
    print("Data Inserted!!")
    msg = "Data Update to: [ {} ] | table: {} | DB: {}".format(set, table, database)

    return render_template('display.html', msg = msg)

# MySQL - Delete From Table
@app.route('/deleteTable/<host>/<user>/<passwd>', methods = ['POST'])
def deleteTable(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    where = request.form['WHERE']
    
    query = "DELETE FROM " + table + " WHERE " + where
    print(query)
    mydb = connection.connect(host=host, database=database, user=user, passwd=passwd, use_pure=True)
    cursor = mydb.cursor()  # create a cursor to execute queries
    cursor.execute(query)
    mydb.commit()
    print("Data Deleted!!")
    msg = "Data Deleted: [ {} ] | table: {} | DB: {}".format(where, table, database)

    return render_template('display.html', msg = msg)

# MySQL - Download Table
@app.route('/downloadTable/<host>/<user>/<passwd>', methods = ['POST'])
def downloadTable(host, user, passwd):
    database = request.form['database']
    table = request.form['table']
    file = request.form['file']
    
    mydb = connection.connect(host=host, database=database, user=user, passwd=passwd, use_pure=True)
    query_select = "SELECT * FROM " + table
    pd_result = pd.read_sql(query_select, mydb)
    pd_result.to_csv(file)

    print("Table Downloaded!!")
    msg = "Table Downloaded: [ {} ] | From DB: {}".format(table, database)

    return render_template('display.html', msg = msg)
    
@app.route('/mysql')  
def mySQL():
    return render_template('mysql.html', title = 'MySQL')

@app.route('/mongodb')  
def mongoDB():
    return render_template('mongoDB.html', title = 'MongoDB')

@app.route('/mongodb_cilent', methods = ['POST'])
def mongodb_cilent():
    clientURL = request.form['client']
    #clientConn = mongodbConn(clientURL)
    clientConn = pymongo.MongoClient(clientURL)
    #clientConn = pymongo.MongoClient(clientURL)
    db_list = clientConn.list_database_names()
    return render_template('mongodb_operation.html', clientConn = clientConn, db_list = db_list, total_db = len(db_list))

# MySQL - Identify the Operation
@app.route('/mongodb_SelectOperation/<clientConn>', methods = ['POST'])
def mongodb_SelectOperation(clientConn):
    

    operation = request.form['operation']
    print(operation)
    if operation == 'insert_one':
        return render_template('mysql.html', title = 'MySQL')
        #return render_template('md_insert_one.html', clientConn=clientConn, title = 'post')
    elif operation == 'insert_bulk':
            return render_template('md_insert_bulk.html', clientConn=clientConn, title = 'post')
    elif operation == 'update':
        return render_template('md_updateTable.html', clientConn=clientConn, title = 'post')
    elif operation == 'delete':
        return render_template('md_deleteTable.html', clientConn=clientConn, title = 'post')
    elif operation == 'download':
        return render_template('md_downloadTable.html', clientConn=clientConn, title = 'post')


if __name__ == '__main__':  
    app.run(debug=True)