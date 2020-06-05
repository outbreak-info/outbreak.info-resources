import os
import csv
import sqlite3
import json

def import_categories(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    categories = ['Behavioral Research', 'Behavioral Research', 'Clinical', 'Risk Factors', 
        'Antibody Detection', 'Diagnosis', 'Pathology/Radiology', 'Rapid Diagnostics', 
        'Symptoms', 'Testing Prevalence', 'Virus Detection', 'Classical epidemiology', 
        'Epidemiology', 'Molecular epidemiology', 'Forecasting', 'Host Factors', 
        'Immunological Response', 'Mechanism', 'Mechanism of Infection',
        'Mechanism of Transmission', 'Virus Factors', 'Individual Prevention', 'Prevention', 
        'Public Health Interventions', 'Host/Intermediate Reservoirs', 'Transmission', 
        'Viral Shedding / Persistence', 'Biologics', 'Medical Care', 
        'Pharmaceutical Treatments', 'Repurposing', 'Treatment', 'Vaccines']

    c.execute(""" delete from Categories """)

    for category in categories:
        c.execute("""insert into Categories (name) values (?)""", (category,))

    conn.commit()
    c.close()
    conn.close()

    return

def import_documents(db_file, json_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute(""" delete from Datasets """)

    with open(json_file, 'r') as fin:
        datas = json.load(fin)
        for data in datas:
            keywords = ''
            if not data['keywords'] is None:
                keywords = ','.join(data['keywords'])
            
            c.execute("""select count(1) from Datasets where DocumentId = ?""", (data['_id'],))
            if c.fetchone()[0] == 0:
                c.execute("""insert into Datasets 
                (DocumentId,Name,Description,Keywords) values 
                (?,?,?,?)""", (data['_id'], data['name'],data['description'],keywords))

    conn.commit()
    c.close()
    conn.close()

def main():
    import_categories('classifications.db')
    import_documents('classifications.db', 'outbreak_dataset_sample.json')

if __name__ == "__main__":
    main()