import yaml
import os

class Schema:
    def __init__(self, id):
        self.context = {}
        self.graph = []
        self.id = id

    def add_to_context(self, name, url):
        # issue 30. 
        if not url.endswith("/"):
            url = url + "/"
        self.context[name] = url

    def add_to_props(self, prop):
        self.graph.append(prop)

    def clean_cardinality(self, result):
        for dict in result["@graph"]: 
            if "owl:cardinality" in dict:
                cardinality = dict["owl:cardinality"]
                if "one" in cardinality.lower():
                    cardinality = "one"
                else:
                    cardinality = "many"

    def render(self, out):
        result = {}
        result["@context"] = self.context
        result["@id"] = self.id
        result["@graph"] = self.graph

        # do cleansing
        self.clean_cardinality(result)

        # write out
        with open(out, 'w') as fout: 
            fout.write(yaml.dump(result))