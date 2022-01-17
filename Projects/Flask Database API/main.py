from re import T
from turtle import title
from flask import Flask, render_template, request
import json
import mysql.connector as connection
import csv
import pandas as pd
import pymongo
import cassandra

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def cassandraConnect(clientID, clientSecret):
    try:
        cloud_config= {
        'secure_connect_bundle': 'secure-connect-db1.zip' ## Current path (jupyter)
        }
        auth_provider = PlainTextAuthProvider(clientID, clientSecret)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()
        row = session.execute("select release_version from system.local").one()

    except Exception as e:
        print("An Error Occured: ", e)
    else:
        print(row[0])
        return session

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
        elif db_select == 'Cassandra':
            return render_template('cassandra.html', title='Cassandra')

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

    clientURL = clientURL.replace('/', '<123><321>')
    return render_template('mongodb_operation.html', clientConn = clientConn, clientURL=clientURL,db_list = db_list, total_db = len(db_list))

# MySQL - Identify the Operation
@app.route('/mongodb_SelectOperation/<clientConn>/<clientURL>', methods = ['POST'])
def mongodb_SelectOperation(clientConn, clientURL):
    
    #clientURL = clientURL.replace('<123><321>', '/')

    operation = request.form['operation']

    if operation == 'insert_one':
        return render_template('md_insert_one.html', clientConn=clientConn, clientURL=clientURL, title = 'post')
    elif operation == 'insert_bulk':
        return render_template('md_insert_bulk.html', clientConn=clientConn, clientURL=clientURL, title = 'post')
    elif operation == 'update':
        return render_template('md_update.html', clientConn=clientConn, clientURL=clientURL,title = 'post')
    elif operation == 'delete':
        return render_template('md_delete.html', clientConn=clientConn, clientURL=clientURL, title = 'post')
    elif operation == 'drop':
        return render_template('md_drop.html', clientConn=clientConn, clientURL=clientURL, title = 'post')

# MongoDB - Insert One
@app.route('/md_insertOne/<clientConn>/<clientURL>', methods = ['POST'])
def md_insertOne(clientConn, clientURL):
    database = request.form['database']
    dbCollection = request.form['dbCollection']

    record = request.form['record']                 # Record is in string format
    record = record.replace("'", '"')               # Replacing the single-quotes to double-quotes for json.loads
    record  = json.loads(record)                    # Converting the string into json dict format

    clientURL = clientURL.replace('<123><321>', '/')

    clientConn = pymongo.MongoClient(clientURL)     # connection with mongoDB
    db_local = clientConn[database]                 # Creating a database over the client
    collection_local = db_local[dbCollection]       # Creating a collection over the database

    collection_local.insert_one(record)

    #mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Record Inserted!!")
    msg = "Record inserted into Collection: {} | DB: {}".format(database, dbCollection)

    return render_template('display.html', msg = msg)

# MongoDB - Insert Many
@app.route('/md_insertMany/<clientConn>/<clientURL>', methods = ['POST'])
def md_insertMany(clientConn, clientURL):
    database = request.form['database']
    dbCollection = request.form['dbCollection']

    record = request.form['record']                 # Record is in string format
    record = record.replace("'", '"')               # Replacing the single-quotes to double-quotes for json.loads
    record = record.split(', ')
    rec = []
    for i in record:                                # Creating the list of dict
        print(i, type(i))
        r = json.loads(str(i))
        rec.append(r)

    clientURL = clientURL.replace('<123><321>', '/')

    clientConn = pymongo.MongoClient(clientURL)     # connection with mongoDB
    db_local = clientConn[database]                 # Creating a database over the client
    collection_local = db_local[dbCollection]       # Creating a collection over the database

    collection_local.insert_many(rec)

    #mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Record Inserted!!")
    msg = "Record inserted into Collection: {} | DB: {}".format(database, dbCollection)

    return render_template('display.html', msg = msg)

# MongoDB - Update Record
@app.route('/md_update/<clientConn>/<clientURL>', methods = ['POST'])
def md_update(clientConn, clientURL):
    database = request.form['database']
    dbCollection = request.form['dbCollection']
    set = request.form['SET']
    where = request.form['WHERE']

    set = set.replace("'", '"')             
    set  = json.loads(set)  
    set = {"$set": set}
    where = where.replace("'", '"')             
    where  = json.loads(where)  

    clientURL = clientURL.replace('<123><321>', '/')

    clientConn = pymongo.MongoClient(clientURL)     # connection with mongoDB
    db_local = clientConn[database]                 # Creating a database over the client
    collection_local = db_local[dbCollection]       # Creating a collection over the database

    collection_local.update_one(where, set)

    #mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Record Updated!!")
    msg = "Record Update on  Collection: {} | DB: {}".format(database, dbCollection)

    return render_template('display.html', msg = msg)

# MongoDB - Update Record
@app.route('/md_delete/<clientConn>/<clientURL>', methods = ['POST'])
def md_delete(clientConn, clientURL):
    database = request.form['database']
    dbCollection = request.form['dbCollection']
    where = request.form['WHERE']

    where = where.replace("'", '"')             
    where  = json.loads(where)  

    clientURL = clientURL.replace('<123><321>', '/')

    clientConn = pymongo.MongoClient(clientURL)     # connection with mongoDB
    db_local = clientConn[database]                 # Creating a database over the client
    collection_local = db_local[dbCollection]       # Creating a collection over the database

    collection_local.delete_one(where)

    #mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Record Deleted!!")
    msg = "Record Deleted in  Collection: {} | DB: {}".format(database, dbCollection)

    return render_template('display.html', msg = msg)

# MongoDB - Drop Collection
@app.route('/md_drop/<clientConn>/<clientURL>', methods = ['POST'])
def md_drop(clientConn, clientURL):
    database = request.form['database']
    dbCollection = request.form['dbCollection']
 
    clientURL = clientURL.replace('<123><321>', '/')

    clientConn = pymongo.MongoClient(clientURL)     # connection with mongoDB
    db_local = clientConn[database]                 # Creating a database over the client
    collection_local = db_local[dbCollection]       # Creating a collection over the database

    collection_local.drop()

    #mysql_basic(host=host, user=user, passwd=passwd, database=database, query=query, commit = True)
    print("Collection Dropped!!")
    msg = "Collection Dropped DB: {}".format(dbCollection)

    return render_template('display.html', msg = msg)

@app.route('/cassandra')  
def cassandra():
    return render_template('cassandra.html', title='Cassandra')

@app.route('/cassConnection', methods = ['POST'])
def cassConnection():
    id = request.form['clientID']
    secret = request.form['clientSecret']

    session = cassandraConnect(id, secret)

    row=session.execute("SELECT * FROM system_schema.keyspaces;")
    keyspaceList = []
    for i in row:
        keyspaceList.append(i[0])

    return render_template('cassOperation.html', id = id, secret=secret,keyspaceList = keyspaceList, total_ks = len(keyspaceList))

# Cassandra - Identify the Operation
@app.route('/cassExecute/<id>/<secret>', methods = ['POST'])
def cassExecute(id, secret):

    try:
        operation = request.form['operation']
        #print(operation)
        if operation == 'create_table':
            return render_template('cassCreateTable.html', id=id, secret=secret, title = 'post')
        elif operation == 'insert_one':
            return render_template('cassInsert_one.html', id=id, secret=secret, title = 'post')
        elif operation == 'insert_bulk':
             return render_template('cassInsert_bulk.html', id=id, secret=secret, title = 'post')
        elif operation == 'update':
            return render_template('cassUpdateTable.html', id=id, secret=secret, title = 'post')
        elif operation == 'delete':
            return render_template('cassDeleteTable.html', id=id, secret=secret, title = 'post')
        elif operation == 'download':
            return render_template('cassDownloadTable.html', id=id, secret=secret, title = 'post')
        else:
            return render_template('cassandra.html')

    except Exception as e:
        print(str(e))

@app.route('/cassCreateTable/<id>/<secret>', methods = ['POST'])
def cassCreateTable(id, secret):
    keyspace = request.form['keyspace']
    table = request.form['table']
    attr = request.form['attr']

    session = cassandraConnect(id, secret)
    # session.execute("CREATE TABLE keyspace2.table1(id int PRIMARY KEY,name text,age int,height int);")
    query = "CREATE TABLE " + keyspace + "." + table + attr + ";"
    session.execute(query)
    
    msg = "Table Create"
    return render_template('display.html', msg = msg)

@app.route('/cassInsertRecord/<id>/<secret>', methods = ['POST'])
def cassInsertRecord(id, secret):
    keyspace = request.form['keyspace']
    table = request.form['table']
    attr = request.form['attr']
    data = request.form['data']

    session = cassandraConnect(id, secret)
    # row=session.execute("INSERT INTO keyspace2.table1(id,name,age,height) VALUES (1,'mohit',25,160);")
    #query = "INSERT INTO " + keyspace + "." + table + attr + " VALUES " + data + ";"
    query = "INSERT INTO {}.{}{} VALUES {};".format(keyspace,table,attr,data)
    session.execute(query)
    
    msg = "Record inserted into Collection: {}".format(keyspace)

    return render_template('display.html', msg = msg)

@app.route('/cassInsertBulk/<id>/<secret>', methods = ['POST'])
def cassInsertBulk(id, secret):
    keyspace = request.form['keyspace']
    table = request.form['table']
    attr = request.form['attr']
    path = request.form['path']

    session = cassandraConnect(id, secret)

    with open(path,'r') as data:
        next(data)
        data_csv= csv.reader(data,delimiter=',')
        #csv reader object
        print(data_csv)
        all_value= []
        for i in data_csv:
            s = ""
            for j in i:
                s = s + j + ','
            s = s[0:len(s)-1]
            query = "INSERT INTO {}.{}{} VALUES ({})".format(keyspace, table, attr, s)
            print(query)
            session.execute(query)

    msg = "Record inserted into Collection: {}".format(keyspace)
    return render_template('display.html', msg = msg)

@app.route('/cassUpdateTable/<id>/<secret>', methods = ['POST'])
def cassUpdateTable(id, secret):
    keyspace = request.form['keyspace']
    table = request.form['table']
    set = request.form['SET']
    where = request.form['WHERE']

    session = cassandraConnect(id, secret)

    query = "UPDATE {}.{} SET {} WHERE {};".format(keyspace,table,set,where)
    session.execute(query)

    msg = "Record update into Collection: {}".format(keyspace)
    return render_template('display.html', msg = msg)

@app.route('/cassDeleteData/<id>/<secret>', methods = ['POST'])
def cassDeleteData(id, secret):
    keyspace = request.form['keyspace']
    table = request.form['table']
    where = request.form['WHERE']

    session = cassandraConnect(id, secret)

    query = "DELETE FROM {}.{} WHERE {};".format(keyspace,table,where)
    session.execute(query)

    msg = "Record deleted from Collection: {}".format(keyspace)
    return render_template('display.html', msg = msg)

if __name__ == '__main__':  
    app.run(debug=True) 