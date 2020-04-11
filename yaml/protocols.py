from schema import Schema
import os
import csv

schema = Schema("http://sulab.org/")

schema.add_to_context("schema", "http://schema.org")
schema.add_to_context("bioschemas", "http://bioschema.org")
schema.add_to_context("owl", "http://www.w3.org/2002/07/owl")

with open("c:/users/ben/desktop/schemas/protocol.csv", "r") as fin:
    csv_reader = csv.reader(fin)

    cols = []
    for row in csv_reader:
        if len(cols) == 0:
            cols = row
        else:   
            prop = {}
            prop["@id"] = row[cols.index("Property")]
            prop["@type"] = "rdf:Property"
            #prop["rdfs:subClassOf"] = {"@id" : row[cols.index("sameAs")].lower()}

            subClassOf = row[cols.index("sameAs")]
            subClassOf = [f.strip() for f in subClassOf.replace('[', '').replace(']','').split(',')]

            if len(subClassOf) == 1:
                prop["rdfs:subClassOf"] = {"@id" : subClassOf[0]}
            else:
                prop["rdfs:subClassOf"] = [{"@id" : f} for f in subClassOf]


            prop["rdfs:comment"] = row[cols.index("Description")]
            prop["owl:cardinality"] = row[cols.index("cardinality")]
            prop["marginality"] = row[cols.index("marginality")]

            rangeIncludes = row[cols.index("expected type")]
            rangeIncludes = [f.strip() for f in rangeIncludes.replace('[', '').replace(']','').split(',')]

            if len(rangeIncludes) == 1:
                prop["schema:rangeIncludes"] = {"@id" : rangeIncludes[0]}
            else:
                prop["schema:rangeIncludes"] = [{"@id" : f} for f in rangeIncludes]
            

            schema.add_to_props(prop)

schema.render('C:/Users/ben/Desktop/schemas/protocols.yaml')
