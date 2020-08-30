import requests
import pandas as pd

API = "https://api.outbreak.info/resources"

"""
Pulls a random sample of n datasets from EACH different dataset source.
Note: a.t.m. there's a bit of a hack for Zenodo, since it isn't capturing `curatedBy.name: Zenodo`
Saves the result either as a .json or .tsv and returns a Pandas DataFrame
"""
def sampleDatasets(url, n = 3, type = "Dataset", sources = ["The Protein Data Bank", "Figshare", "litcovid", "medrxiv", "biorxiv", "ClinicalTrials.gov", "WHO International Clinical Trials Registry Platform", "Zenodo"], fields = ["name", "description", "abstract", "keywords"], filename="outbreak_dataset_sample.json", output = "json"):
    df = pd.DataFrame()
    field_string = ",".join(fields)

    for source in sources:
        query = f'{url}/query?q=@type:{type} AND curatedBy.name:"{source}"&fields={field_string}'
        print(f"\nGetting sample from {source}")
        df_sample = pullSample(query, n, source)
        df = pd.concat([df, df_sample], ignore_index=True, sort=False)

    print("Querying just the Zenodo data...")
    zquery = f'{url}/zenodo/query?q=@type:{type}&fields={field_string}'
    df_sample = pullSample(zquery, n, "Zenodo")
    df = pd.concat([df, df_sample], ignore_index=True, sort=False)

    print("Done sampling data!")

    df["description_abstract"] = df.apply(getDescription, axis=1)

    if(output == "json"):
        df.to_json(filename, orient="records")
    elif(output == "tsv"):
        df.to_csv(filename, index=False, sep="\t")
    elif((output.lower() == "excel") | (output == "xls") | (output == "xlsx")):
        df.to_excel(filename)
    else:
        print("Unknown output type supplied. Please use 'json' or 'tsv'")
    return(df)


def getDescription(row):
    if(row.description == row.description):
        return(row.description)
    elif(row.abstract == row.abstract):
        return(row.abstract)

"""
Requires `fetch_all` parameter to get more than 1,000 records.
"""
def pullSample(query, n, source):
    df = pd.DataFrame()
    res = getOneRecord(query, source)

    while(res is not None):
        if(res["page"]*1000 + 1 > res["total"]):
            lower = res["total"]
        else:
            lower = res["page"]*1000 + 1
        if((res["page"] + 1)*1000 > res["total"]):
            upper = res["total"]
        else:
            upper = (res["page"] + 1)*1000
        print(f'Fetched results {lower} - {upper} of {res["total"]}')
        df = pd.concat([df, res["data"]], ignore_index=True, sort=False)
        res = getOneRecord(query, source, res["id"], res["page"])
    if(len(df) >= n):
        df.drop("_score", axis=1, inplace=True)
        return(df.sample(n, random_state=25))
    else:
        print(f"You asked for too large a sample! Returning {len(df)} records for {source}")
        return(df)

def getOneRecord(query, source, scroll_id=None, query_num=-1):
    # print(f"Executing query #{query_num}")
    query = f"{query}&fetch_all=true&query={query_num}"
    if(scroll_id is not None):
        query = f"{query}&fetch_all=true&scroll_id={scroll_id}"
    resp = requests.get(query)

    if(resp.status_code == 200):
        md = resp.json()
        if("hits" in md.keys()):
            df = pd.DataFrame(md["hits"])
            df["source"] = source
            return({"data": df, "id": md["_scroll_id"], "page": query_num+1, "total": md["total"]})
        else:
            return(None)
    else:
        raise ValueError(f"Query {query} resulted in a {resp.status_code} error")


sampleDatasets(API, type="Dataset", n=10)
sampleDatasets(API, type="Publication")