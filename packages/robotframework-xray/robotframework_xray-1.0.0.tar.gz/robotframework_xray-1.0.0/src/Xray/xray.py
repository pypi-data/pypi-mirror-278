import os, json, requests
from os.path import join
from datetime import datetime
from .config import Config

class Xray:
    def authentication() -> str:
        XRAY_API = Config.xray_api()
        XRAY_CLIENT_ID = Config.xray_client_id()
        XRAY_CLIENT_SECRET = Config.xray_client_secret()

        json_data = json.dumps({'client_id': XRAY_CLIENT_ID, 'client_secret': XRAY_CLIENT_SECRET})
        resp = requests.post(f'{XRAY_API}/authenticate', data=json_data, headers={'Content-Type':'application/json'})
            
        if resp.status_code == 200:
            return f'Bearer {resp.json()}'
        else:
            print('Authentication error, trying again...')
            Xray.authentication()

    def updateXrayTest(issueId: str, unstructured: str):
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()
        unstructured = unstructured.encode('unicode_escape').decode()
        unstructured = unstructured.replace('    ', '\\t')
        unstructured = unstructured.replace('"', '\\"')
        
        json_data = f'''
            mutation {{
                updateUnstructuredTestDefinition(issueId: "{ issueId }", unstructured: "{ unstructured }") {{
                    issueId
                    unstructured
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        if resp.status_code == 200:
            return resp.json()
        else:
            print('Error updating xray test, trying again...')
            Xray.updateXrayTest(issueId, unstructured)

    def updateXrayTestType(issueId: str):
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()
        
        json_data = f'''
            mutation {{
                updateTestType(issueId: "{ issueId }", testType: {{ name: "Generic" }} ) {{
                    issueId
                    testType {{
                        name
                        kind
                    }}
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        if resp.status_code != 200:
            print('Error updating xray test type, trying again...')
            Xray.updateXrayTestType(issueId)
    
    def addEvidenceToTestRun(id: int, filename: str, data: str):
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()

        json_data = f'''
            mutation {{
                addEvidenceToTestRun(
                    id: "{ id }",
                    evidence: [
                        {{
                            filename: "{ filename }"
                            mimeType: "video/webm"
                            data: "{ data }"
                        }}
                    ]
                ) {{
                    addedEvidence
                    warnings
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        if resp.status_code != 200:
            print('Error sending evidence, trying again...')
            Xray.addEvidenceToTestRun(id, filename, data)

    def getTest(testKey: str):
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()

        json_data = f'''
            {{
                getTests(
                    jql: "key = '{ testKey }'",
                    limit: 1
                ) {{
                    results {{
                        issueId
                    }}
                }}
            }}
        '''

        resp = requests.get(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        if resp.status_code == 200:
            return resp.json().get('data').get('getTests').get('results')[0].get('issueId')
        else:
            print('Error getting test ID, trying again...')
            Xray.getTest(testKey)
    
    def getTestRun(testIssueId: str, testExecutionIssueId: str):
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()

        json_data = f'''
            {{
                getTestRun(
                    testIssueId: "{ testIssueId }",
                    testExecIssueId: "{ testExecutionIssueId }"
                ) {{
                    id
                }}
            }}
        '''

        resp = requests.get(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        if resp.status_code == 200:
            return resp.json().get('data').get('getTestRun').get('id')
        else:
            print('Error getting run ID, retrying...')
            Xray.getTestRun(testIssueId, testExecutionIssueId)
    
    def createTestExecution():
        PROJECT_KEY = Config.project_key()
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()
        test_execution_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        json_data = f'''
            mutation {{
                createTestExecution(
                    testIssueIds: [],
                    testEnvironments: [],
                    jira: {{
                        fields: {{
                            summary: "QA Automation Execution | { test_execution_date }",
                            project: {{ key: "{ PROJECT_KEY }" }}
                        }}
                    }}
                ) {{
                    testExecution {{
                        issueId
                        jira(fields: ["key"])
                    }}
                    warnings
                    createdTestEnvironments
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': auth_token
            },
        )

        result = json.dumps({
            'issueId': resp.json().get('data').get('createTestExecution').get('testExecution').get('issueId'),
            'key': resp.json().get('data').get('createTestExecution').get('testExecution').get('jira').get('key')
        })

        if resp.status_code == 200:
            return json.loads(result)
        else:
            print('Error create test execution, trying again...')
            Xray.createTestExecution()
    
    def importExecutionRobot():
        PROJECT_KEY = Config.project_key()
        XRAY_API = Config.xray_api()

        auth_token = Xray.authentication()
        testExecKey = Xray.createTestExecution()

        report = requests.post(f'{XRAY_API}/import/execution/robot', 
            data=open(join(os.path.abspath(os.curdir), 'report.xml'), 'rb'),
            params={
                'projectKey': PROJECT_KEY,
                'testExecKey': testExecKey['key'],
            },
            headers={
                'Content-Type': 'application/xml',
                'Authorization': auth_token
            }
        )

        resp = json.dumps({
            'issueId': testExecKey['issueId'],
            'key': report.json().get('key')
        })

        if report.status_code == 200:
            return json.loads(resp)
        else:
            print('Error import execution, trying again...')
            Xray.importExecutionRobot()