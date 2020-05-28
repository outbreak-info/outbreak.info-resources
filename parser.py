import requests
import json

DATAVERSE_SERVERS = [
  "https://dataverse.harvard.edu/api/",
]
# Are there other Dataverse servers?

SERVER  = "https://dataverse.harvard.edu/api/"
EXPORT_URL = f"{SERVER}datasets/export?exporter=schema.org"
QUERIES = ["sars-cov-2", "covid-19"]

def compile_query(server, queries=None, response_types=None, subtrees=None):
  """
  Queries are string queries, e.g., "COVID-19"
  Response types are e.g., "dataverse", "dataset", "file"
  Subtrees are specific dataverse IDs

  All can have multiple values. Response types and subtrees are OR'd
  Queries are probably OR'd
  """

  query_string   = ""
  type_string    = ""
  subtree_string = ""

  if queries:
    # turn ["a", "b"] into '"a"+"b"'
    query_string = "+".join(f"\"{q}\"" for q in queries)

  if response_types:
    type_string  = "".join(f"&type={r}" for r in response_types)

  if subtrees:
    subtree_string = "".join(f"&subtree={s}" for s in subtrees)

  return f"{server}search?q={query_string}{type_string}{subtree_string}"

def compile_paginated_data(query_endpoint, per_page=100):
  """
  pages through data, compiling all response['data']['items']
  and returning them.
  per_page max is 1000
  """

  continue_paging = True
  start = 0
  data = []

  while continue_paging:
    url = f"{query_endpoint}&per_page={per_page}&start={start}"
    print(f"getting {url}")
    req = requests.get(url)
    response = req.json()
    total = response.get('data').get('total_count')
    data.extend(response.get('data').get('items'))
    start += per_page
    continue_paging = total and start < total

  return data

def find_relevant_dataverses():
  response_types = ["dataverse"]
  query_endpoint = compile_query(SERVER, QUERIES, response_types)
  dataverses = [data['identifier'] for data
                in compile_paginated_data(query_endpoint)]
  return dataverses

def find_relevant_datasets_and_files(dataverse_id):
  """
  We may not need to search via dataverse_id,
  or can group all dataverse IDs into a singular batch of requests
  """

  response_types = ["dataset", "file"]
  query_endpoint = compile_query(SERVER,
      QUERIES, # not sure if we should search these queries here, since the dataverse showed up for these queries already
      response_types=response_types,
      subtrees=[dataverse_id])
  datasets_and_files = compile_paginated_data(query_endpoint)
  return datasets_and_files

if __name__ == "__main__":
  """
  dataverses = find_relevant_dataverses()
  datasets_and_files = []
  for dataverse in dataverses:
    datasets_and_files.extend(find_relevant_datasets_and_files(dataverse))
  datasets = [d for d in datasets_and_files if d['type'] == 'dataset']
  """
  dataset_endpoint = compile_query(SERVER, QUERIES, response_types=["dataset"])
  datasets = compile_paginated_data(dataset_endpoint)
  schema_org_exports = []

  for dataset in datasets:
    schema_export_url = f"{EXPORT_URL}&persistentId={dataset['global_id']}"
    req = requests.get(schema_export_url)
    res = req.json()
    if res.get('status') and res.get('status') == 'ERROR':
      print(f"{dataset['name']} could not be exported")
      continue
    schema_org_exports.append(res)
