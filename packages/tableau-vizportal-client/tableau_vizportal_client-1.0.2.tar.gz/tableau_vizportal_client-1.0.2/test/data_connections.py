import csv
import tableauserverclient as TSC
from config import PAT_NAME, PAT_VALUE, URL, SITE

server = TSC.Server(URL)
server.version = "3.11"
server.add_http_options({"verify": False})
tableau_auth = TSC.PersonalAccessTokenAuth(PAT_NAME, PAT_VALUE, site_id=SITE)


all_connections = []
with server.auth.sign_in_with_personal_access_token(tableau_auth):
    datasources = TSC.Pager(server.datasources)
    for datasource in datasources:
        server.datasources.populate_connections(datasource)
        for connection in datasource.connections:
            details = [connection.connection_type, connection.server_address, connection.server_port]
            all_connections.append(details)


with open("data_connections.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["connectionType","serverName", "serverPort"])
    for r in all_connections:
        writer.writerow(r)