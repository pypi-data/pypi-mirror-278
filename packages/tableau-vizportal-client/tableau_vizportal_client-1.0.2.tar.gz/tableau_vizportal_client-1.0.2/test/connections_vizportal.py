from pprint import pprint
import csv
from vizportal import VizportalPager
import tableauserverclient as TSC
from typing import Dict, Any, List
from vizportal.helpers import merge_results_by_keys
from config import PAT_NAME, PAT_VALUE, URL, SITE

server: TSC.Server = TSC.Server(URL)
server.version = "3.11"
server.add_http_options({"verify": False})
tableau_auth: TSC.PersonalAccessTokenAuth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_VALUE, site_id=SITE)

EXCLUDE_CONNECTION_TYPES: List[str] = ["hyper", "excel-direct", "textscan"]

with server.auth.sign_in_with_personal_access_token(tableau_auth):
    payload: Dict[str, Any] = {
        "method": "getDataConnections",
        "params": {
            "filter": {
                "operator": "and",
                "clauses": [
                    {"operator": "eq", "field": "isPublished", "value": True},
                    {"operator": "eq", "field": "containerType", "value": "datasource"},
                ],
            },
            "order": [{"field": "name", "ascending": True}],
            "page": {"startIndex": 0, "maxItems": 600},
        },
    }

    results: VizportalPager = VizportalPager(server, payload)
    merged_results: Dict[str, Any] = merge_results_by_keys(results, ["dataConnections", "datasources"])

    combined: List[Dict[str, Any]] = []
    
    all_connections: List[Dict[str, Any]] = merged_results["dataConnections"]
    for connection in all_connections:
        if connection["connectionType"] not in EXCLUDE_CONNECTION_TYPES:
            connection_details: Dict[str, Any] = connection["connectionDetails"]
            connection_details["connectionType"] = connection["connectionType"]
            combined.append(connection["connectionDetails"])

with open("connections.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["connectionType","serverName", "serverPort", "type"])
        for r in combined:
            wb: List[Any] = [r.get("connectionType"), r.get("serverName"), r.get("serverPort"), r.get("type")]
            writer.writerow(wb)
