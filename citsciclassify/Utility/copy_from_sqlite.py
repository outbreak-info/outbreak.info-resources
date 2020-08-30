import sqlite3
from sqlite3 import Error
import mysql.connector
import os
import datetime

def main():
    sqlite_conn = sqlite3.connect('../Flask/classifications.db')
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="7%jqpwB{#G+D9j",
        database="citsciclassify",
    )

    user_id_dict = {}
    category_id_dict = {}
    dataset_id_dict = {}
    usercompleted_Datasets_id_dict = {}

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    print("Clearing existing records...")
    mysql_cursor.execute(""" delete from UserCompletedDatasetClassifications""")
    mysql_cursor.execute(""" delete from UserCompletedDatasets""")
    mysql_cursor.execute(""" delete from Datasets """)
    mysql_cursor.execute(""" delete from Categories""")
    mysql_cursor.execute(""" delete from Users """)

    # copy over all the Users
    print("Copying over Users...")
    sqlite_cursor.execute("""select Email, Name, Id from Users""")
    results = sqlite_cursor.fetchall()
    
    for result in results:
        user_email, user_name, sqlite_id = result
        
        mysql_cursor.execute("""insert into Users (email, name) values (%s, %s)""", (user_name, user_email))

        mysql_cursor.execute("""select last_insert_id()""")
        user_id_dict[sqlite_id] = mysql_cursor.fetchone()[0]

    # copy over all the Categories
    print("Copying over Categories....")
    sqlite_cursor.execute(""" select name, id from Categories""")
    results = sqlite_cursor.fetchall()

    
    for result in results:
        name, sqlite_id = result
        mysql_cursor.execute("""insert into Categories (name) value (%s)""", (name,))

        mysql_cursor.execute("""select last_insert_id()""")
        category_id_dict[sqlite_id] = mysql_cursor.fetchone()[0]

    # copy over the Datasets
    print("Copying over Datasets...")
    sqlite_cursor.execute(""" select documentid, name, description, keywords, id from Datasets""")
    results = sqlite_cursor.fetchall()

    
    for result in results:
        document_id, name, description, keywords, sqlite_id = result

        mysql_cursor.execute("""insert into Datasets (documentid,name,description,keywords) 
            values (%s, %s, %s, %s)""", (document_id, name, description, keywords))

        mysql_cursor.execute("""select last_insert_id()""")
        dataset_id_dict[sqlite_id] = mysql_cursor.fetchone()[0]

    # copy over usercompletedDatasets
    print("Copying over UserCompletedDatasets...")
    sqlite_cursor.execute(""" select userid, completedat, enoughinformation, datasetid, id from UserCompletedDatasets""")
    results = sqlite_cursor.fetchall()

    for result in results:
        userid, completedat, enoughinformation, datasetid, sqlite_id = result

        #08/06/2020, 14:26:11
        completedat_obj = datetime.datetime.strptime(completedat, '%m/%d/%Y, %H:%M:%S')

        mysql_cursor.execute("""insert into usercompletedDatasets (userid,completedat,enoughinformation,datasetid) 
            values (%s, %s, %s, %s)""", (user_id_dict[userid], completedat_obj, enoughinformation, dataset_id_dict[datasetid]))
        mysql_cursor.execute("""select last_insert_id()""")
        usercompleted_Datasets_id_dict[sqlite_id] = mysql_cursor.fetchone()[0]

    # copy over usercompleteddatasetclassifications
    print("Copyig over UserCompletedDatasetClassifications... ")
    sqlite_cursor.execute(""" select categoryid, datasetid, usercompleteddatasetid, userid, rank from UserCompletedDatasetClassifications""")
    results = sqlite_cursor.fetchall()
    
    for result in results:
        categoryid, datasetid, usercompleteddatasetid, userid, rank = result

        mysql_cursor.execute("""insert into usercompleteddatasetclassifications 
            (categoryid, datasetid, usercompleteddatasetid, userid, rank) values (%s, %s, %s, %s, %s)""", 
            (category_id_dict[categoryid], 
            dataset_id_dict[datasetid], 
            usercompleted_Datasets_id_dict[usercompleteddatasetid],
            user_id_dict[userid],
            rank))

    mysql_conn.commit()

    sqlite_conn.close()
    mysql_conn.close()

if __name__ == "__main__":
    # Only for debugging while developing
    main()