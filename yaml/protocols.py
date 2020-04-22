from schema import Schema, ClassProperty
import os
import csv

schema = Schema("http://sulab.org/")

schema.add_to_context("schema", "http://schema.org")
schema.add_to_context("bioschemas", "http://bioschemas.org")
schema.add_to_context("owl", "http://www.w3.org/2002/07/owl")
schema.add_to_context("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns")
schema.add_to_context("rdfs", "http://www.w3.org/2000/01/rdf-schema")
schema.add_to_context("outbreak", "http://outbreak.info/")
schema.add_to_context("prs", "https://prsinfo.clinicaltrials.gov/ProtocolRecordSchema.xsd")

class_dir = "yaml/classes"
class_files = [os.path.join(os.getcwd(), "yaml/classes", f) 
    for f in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, f))]

for class_file in class_files:

    with open(class_file, "r") as fin:
        csv_reader = csv.reader(fin)
        cols = []
        class_props = []
        for row in csv_reader:
            if len(cols) == 0:
                cols = row
            else:   
                class_prop = ClassProperty()
                class_prop.id = "outbreak:" + row[cols.index("Property")]
                class_prop.comment = row[cols.index("Description")]
                class_prop.cardinality = row[cols.index("cardinality")]
                class_prop.marginality = row[cols.index("marginality")]
                class_prop.domain_includes = row[cols.index("domainIncludes")]
                class_prop.label = row[cols.index("Property")]

                rangeIncludes = row[cols.index("expected type")]
                rangeIncludes = [f.strip() for f in rangeIncludes.replace('[', '').replace(']','').split(',')]

                if len(rangeIncludes) == 1:
                    class_prop.range_includes = {"@id" : rangeIncludes[0]}
                else:
                    class_prop.range_includes = [{"@id" : f} for f in rangeIncludes]

                sameAs = row[cols.index("sameAs")]
                sameAs = [f.strip().replace(" ", "") for f in sameAs.replace('[', '').replace(']','').split(',')]

                if len(sameAs) == 1:
                    class_prop.same_as = {"@id" : sameAs[0]}
                else:
                    class_prop.same_as = [{"@id" : f} for f in sameAs]

                class_prop.cardinality = row[cols.index("cardinality")]
                class_prop.marginality = row[cols.index("marginality")]

                class_props.append(class_prop)

        file_name = class_file[class_file.rfind("\\")+1:]
        sub_classes = [s.strip() for s in file_name[file_name.find('(')+1:len(file_name)-5].split(',')]
        class_id = file_name[:file_name.find('(')]

        schema.add_class("outbreak:" + class_id, class_id, class_id, sub_classes, "https://outbreak.org", class_props)


with open("yaml/csvs/protocol.csv", "r") as fin:
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
            prop["schema:domainIncludes"] = {"@id" : "outbreak:Protocol"}

            rangeIncludes = row[cols.index("expected type")]
            rangeIncludes = [f.strip() for f in rangeIncludes.replace('[', '').replace(']','').split(',')]

            if len(rangeIncludes) == 1:
                prop["schema:rangeIncludes"] = {"@id" : rangeIncludes[0]}
            else:
                prop["schema:rangeIncludes"] = [{"@id" : f} for f in rangeIncludes]
            

            schema.add_to_props(prop)

schema.render('yaml/yaml_out/protocols.yaml')
