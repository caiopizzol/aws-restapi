import os
import json
from psycopg2 import connect

RESPONSE = {
    'statusCode': 200,
    'headers': { 'Access-Control-Allow-Origin' : '*' },
    'body': {},
    'isBase64Encoded': False
}


## Lambda handler
def handler(event, context):
    print('event:',event)
    provider_id = event['pathParameters']['id']
    body = json.loads(event['body'])
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Provider id {} was successfully updated!'.format(update_provider(provider_id, body))
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def update_provider(provider_id, body):
    con = get_db_connection()
    cur = con.cursor()
    if len(body.keys()) > 1: #More than 1 field to be updated
        query = '''
        UPDATE providers
        SET ({}) = %s
        WHERE id = %s
        RETURNING id;
        '''.format(', '.join(body.keys()))
    else:
        query = '''
        UPDATE providers
        SET {} = %s
        WHERE id = %s
        RETURNING id;
        '''.format(', '.join(body.keys()))    
    cur.execute(query, (
        tuple(body.values()),
        provider_id
        )
    )
    updated_provider = cur.fetchone()[0]
    con.commit()      
    cur.close()
    if con is not None:
        con.close()
    return updated_provider

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con  

# event = {'resource': '/providers/{id}', 'path': '/providers/2', 'httpMethod': 'PUT', 'headers': None, 'multiValueHeaders': None, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': {'id': '2'}, 'stageVariables': None, 'requestContext': {'resourceId': 'hjltou', 'resourcePath': '/providers/{id}', 'httpMethod': 'PUT', 'extendedRequestId': 'Gqbs6HCCiYcFaQA=', 'requestTime': '04/Oct/2021:03:21:03 +0000', 'path': '/providers/{id}', 'accountId': '689726266135', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1633317663263, 'requestId': 'b60ec0d5-fb1b-42d7-a92b-bae7c4b1cb8a', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws:iam::689726266135:user/caiopizzol', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.12.71 Linux/5.4.134-73.228.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard', 'accountId': '689726266135', 'caller': 'AIDA2BFXDTMLQEKORDNFA', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIA2BFXDTMLVZYJIZ4G', 'cognitoAuthenticationProvider': None, 'user': 'AIDA2BFXDTMLQEKORDNFA'}, 'domainName': 'testPrefix.testDomainName', 'apiId': 'ag40ai9r3i'}, 'body': '{\n    "name": "Transport 1234"\n}', 'isBase64Encoded': False}
# handler(event, {})
