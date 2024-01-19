from sodapy import Socrata

def fetch_data(dataset_identifier, query, app_token=None):
    client = Socrata("data.iowa.gov", app_token, timeout = 30)
    results = client.get(dataset_identifier, query=query)
    return results
