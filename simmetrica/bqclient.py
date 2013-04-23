import httplib2
from apiclient.discovery import build
from oauth2client.appengine import oauth2decorator_from_clientsecrets
from settings import SCOPE
from oauth2client.appengine import AppAssertionCredentials

class BigQueryClient(object):
    def __init__(self):
        # Create a new API service for interacting with BigQuery
        credentials = AppAssertionCredentials(scope=SCOPE)
        http = credentials.authorize(httplib2.Http())
        self.service = build('bigquery', 'v2', http=http)

    def getTableData(self, project, dataset, table):
        # The credentials must already exist before you call decorator.http()
        # So you cannot pre-generate 'decorated' in the BigQueryClient constructor,
        # only from within a method protected by .oauth_required
        return self.service.tables().get(projectId=project, datasetId=dataset,
                                         tableId=table).execute()

    def getLastModTime(self, project, dataset, table):
        data = self.getTableData(project, dataset, table)
        if data is not None and 'lastModifiedTime' in data:
            return data['lastModifiedTime']
        else:
            return None

    def Query(self, query, project, timeout_ms=10000):
        query_config = {
            'query': query,
            'timeoutMs': timeout_ms
        }
        result_json = (self.service.jobs()
                       .query(projectId=project, body=query_config)
                       .execute())

        return result_json
