import yaml
import os
import re

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

    def clean_urls(self, yaml):
        urls = re.findall(r'(?:http|https):\/\/(?:[a-zA-Z0-9\.\/]+)', yaml)
        urls = list(set(urls))
        for url in urls:
            if not url.endswith('/'):
                yaml = yaml.replace(url, url + '/')
        return yaml

    def render(self, out):
        result = {}
        result["@context"] = self.context
        result["@id"] = self.id
        result["@graph"] = self.graph

        # do cleansing
        self.clean_cardinality(result)

        theYaml = yaml.dump(result)
        theYaml = self.clean_urls(theYaml)

        # write out
        with open(out, 'w') as fout: 
            fout.write(theYaml)