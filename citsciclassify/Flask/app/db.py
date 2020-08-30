from flaskext.mysql import MySQL
import os
import datetime

mysql = MySQL()

def initialize_database(app):
    mysql.init_app(app)

def save_classification(user_id, dataset_id, time, enough_information, 
        choice_1, choice_2, choice_3, choice_4, choice_5):
    
    conn = mysql.connect()
    c = conn.cursor()

    time = datetime.datetime.strptime(time, '%m/%d/%Y, %H:%M:%S')

    c.execute(""" insert into UserCompletedDatasets (UserId, DatasetId, CompletedAt, EnoughInformation) values (%s,%s,%s,%s)""", 
        (int(user_id), int(dataset_id), time, enough_information))
    conn.commit()
    
    created_id = c.lastrowid

    if enough_information:
        c.execute(""" insert into UserCompletedDatasetClassifications (CategoryId, DatasetId, UserId, UserCompletedDatasetId, Rank) 
            values (%s,%s,%s,%s,%s)""", (choice_1, dataset_id, user_id, created_id, 1))
        c.execute(""" insert into UserCompletedDatasetClassifications (CategoryId, DatasetId, UserId, UserCompletedDatasetId, Rank) 
                values (%s,%s,%s,%s,%s)""", (choice_2, dataset_id, user_id, created_id, 2))
        c.execute(""" insert into UserCompletedDatasetClassifications (CategoryId, DatasetId, UserId, UserCompletedDatasetId, Rank) 
                values (%s,%s,%s,%s,%s)""", (choice_3, dataset_id, user_id, created_id, 3))
        c.execute(""" insert into UserCompletedDatasetClassifications (CategoryId, DatasetId, UserId, UserCompletedDatasetId, Rank) 
                values (%s,%s,%s,%s,%s)""", (choice_4, dataset_id, user_id, created_id, 4))
        c.execute(""" insert into UserCompletedDatasetClassifications (CategoryId, DatasetId, UserId, UserCompletedDatasetId, Rank) 
                values (%s,%s,%s,%s,%s)""", (choice_5, dataset_id, user_id, created_id, 5))
    conn.commit()

    c.close()
    conn.close()

def get_categories():
    conn = mysql.connect()
    c = conn.cursor()
    c.execute(""" select Id, Name from Categories order by Id asc""")
    results = c.fetchall()
    c.close()
    conn.close()

    return [(r[0],r[1]) for r in results]

def get_dataset_details(document_id):
    conn = mysql.connect()
    c = conn.cursor()

    c.execute(""" select Name, Description, Keywords from Datasets where Id = %s""", (document_id,))
    result = c.fetchone()
    c.close()
    conn.close()

    if len(result) > 0:
        return result[0], result[1], result[2]
    else:
        return None

def get_available_dataset_ids_for_user(user_id):
    conn = mysql.connect()
    c = conn.cursor()

    c.execute("""select Id, DocumentId from Datasets
        where Id not in (select DatasetId from UserCompletedDatasets where UserId = %s)
        and Id not in (select DatasetId from UserCompletedDatasets group by DatasetId having count(*) >= 3)
        order by Id asc""", (user_id,))
    result = c.fetchall()

    c.close()
    conn.close()

    return [(r[0], r[1]) for r in result]

def get_user(user_email, user_name):
    conn = mysql.connect()
    c = conn.cursor()

    c.execute("""select id from users where email = %s""", (user_email,))
    ids = c.fetchall()
    ret = 0
    if len(ids) == 0:
        c.execute("""insert into users ( email, name) values (%s,%s)""", (user_email, user_name))
        conn.commit()
        ret = c.lastrowid
    else:
        ret = ids[0][0]
    c.close()
    conn.close()

    return ret
