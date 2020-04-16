import yaml
import os
import re

class ClassProperty:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.comment = ""
        self.label = ""
        self.domain_includes = ""
        self.range_includes = []
        self.same_as = {}
        self.cardinality = ""
        self.marginality = ""

    def to_dictionary(self):
        ret = {}
        ret["@id"] = self.id
        ret["@type"] = "rdfs:Property"
        ret["rdfs:comment"] = self.comment
        ret["rdfs:label"] = self.label
        ret["schema:domainIncludes"] = {"@id" : self.domain_includes}
        ret["schema:rangeIncludes"] = self.range_includes
        ret["schema:sameAs"] = self.same_as
        ret["owl:cardinality"] = self.cardinality
        ret["marginality"] = self.marginality

        return ret

class Schema:
    def __init__(self, id):
        self.context = {}
        self.graph = []
        self.referenced_classes = []
        self.referenced_class_props = []
        self.id = id

    def add_to_context(self, name, url):
        # issue 30. 
        if not url.endswith("/"):
            url = url + "/"
        self.context[name] = url

    def add_to_props(self, prop):
        self.graph.append(prop)

    def add_class(self, id, comment, label, sub_class, is_part, class_props):
        referenced_class = {}
        referenced_class["@id"] = id
        referenced_class["rdfs:comment"] = comment
        referenced_class["rdfs:label"] = label
        referenced_class["@type"] = "rdfs:Class"

        if len(sub_class) == 1:
            referenced_class["rdfs:subClassOf"] = {"@id" : sub_class[0]}
        else:
            referenced_class["rdfs:subClassOf"] = [{"@id" : f} for f in sub_class]

        referenced_class["rdfs:isPartOf"] = {"@id" : is_part}

        self.referenced_classes.append(referenced_class)

        for class_prop in class_props:
            self.referenced_class_props.append(class_prop.to_dictionary())

    def clean_cardinality(self, result):
        for dict in result["@graph"]: 
            if "owl:cardinality" in dict:
                cardinality = dict["owl:cardinality"]
                if "one" in cardinality.lower():
                    cardinality = "one"
                else:
                    cardinality = "many"

    def clean_urls(self, yaml):
        urls = re.findall(r'(?:http|https):\/\/(?:[a-zA-Z0-9\.\/]+)', yaml)
        urls = list(set(urls))
        for url in urls:
            if not url.endswith('/'):
                yaml = yaml.replace(url, url + '/')
        return yaml

    def enforce_contexts(self, yaml, result):
        namespaces = re.findall(r'([a-zA-Z]+):[a-zA-Z]+', yaml)
        namespaces = list(set(namespaces))
        for namespace in namespaces:
            if not namespace in result["@context"]:
                raise Exception()

    def render(self, out):
        result = {}
        result["@context"] = self.context
        result["@id"] = self.id

        temp_graph = []

        # do this here so they show up first
        for referenced_class in self.referenced_classes:
            temp_graph.append(referenced_class)

        for referenced_class_prop in self.referenced_class_props:
            temp_graph.append(referenced_class_prop)

        self.graph = temp_graph + self.graph

        result["@graph"] = self.graph

        # do cleansing
        self.clean_cardinality(result)

        theYaml = yaml.dump(result)
        theYaml = self.clean_urls(theYaml)

        self.enforce_contexts(theYaml, result)

        # write out
        with open(out, 'w') as fout: 
            fout.write(theYaml)