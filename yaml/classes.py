import os
import csv
import yaml

with open("yaml/classes/outbreak.Dataset.csv", "r") as fin:
    csv_reader = csv.reader(fin)

    cols = []
    graph = []
    result = {}
    for row in csv_reader:
        if len(cols) == 0:
            cols = row
        else:   
            prop = {}

            prop["@id"] = "outbreak:" + row[cols.index("variable name")]
            prop["@type"] = row[cols.index("expected type")]
            prop["marginality"] = row[cols.index("marginality")]
            prop["rdfs:comment"] = row[cols.index("description")]

            subClassOf = row[cols.index("schema.org property")]
            subClassOf = [f.strip() for f in subClassOf.replace('[', '').replace(']','').split(',')]

            if len(subClassOf) == 1:
                prop["rdfs:subClassOf"] = {"@id" : subClassOf[0]}
            else:
                prop["rdfs:subClassOf"] = [{"@id" : f} for f in subClassOf]            

            prop["owl:cardinality"] = row[cols.index("cardinality")]

            graph.append(prop)

    result["@graph"] = graph

    theYaml = yaml.dump(result)

    with open("C:/users/ben/desktop/output.yaml", 'w') as fout: 
            fout.write(theYaml)

    