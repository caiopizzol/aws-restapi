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
    service_area_id = event['pathParameters']['id']
    body = json.loads(event['body'])
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Service area id {} was successfully updated!'.format(update_service_area(service_area_id, body))
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def update_service_area(service_area_id, body):
    con = get_db_connection()
    cur = con.cursor()
    if len(body.keys()) > 1: #More than 1 field to be updated
        query = '''
        UPDATE providers_service_areas
        SET ({}) = %s
        WHERE id = %s
        RETURNING id;
        '''.format(', '.join(body.keys()))
    else:
        query = '''
        UPDATE providers_service_areas
        SET {} = %s
        WHERE id = %s
        RETURNING id;
        '''.format(', '.join(body.keys())) 
    cur.execute(query, (
        tuple(body.values()),
        service_area_id
        )
    )
    updated_service_area = cur.fetchone()[0]
    con.commit()
    cur.close()
    if con is not None:
        con.close()
    return updated_service_area
    

def get_db_connection():         
    # dbname = os.environ["DBNAME"]
    # dbuser = os.environ["DBUSER"]
    # dbpass = os.environ["DBPASS"]
    # dbhost = os.environ["DBHOST"]
    # dbport = os.environ["DBPORT"]
    dbname = 'mozio_db'
    dbuser = 'mozio_user'
    dbpass = 'Ey5hJB9eC83mQdDNemMT'
    dbhost = 'database.chjmfr08q5kt.us-east-2.rds.amazonaws.com'
    dbport = 5432

    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con
    
event =  {'resource': '/service_areas/{id}', 'path': '/service_areas/2', 'httpMethod': 'PUT', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,it;q=0.5,la;q=0.4,ru;q=0.3', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'BR', 'content-type': 'application/json', 'Host': 'ag40ai9r3i.execute-api.us-east-2.amazonaws.com', 'origin': 'chrome-extension://biemppheiopfggogojnfpkngdkchelik', 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'none', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 'Via': '2.0 9a0470365001a35d1ab4fa1b7a9f9daf.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': '062XBuvUWRGcLRKCPHi85Xeguol6MCGvpUr6PMBmtvUk964lx9zv2A==', 'X-Amzn-Trace-Id': 'Root=1-615a80b3-38d82b1d321a2bc35e373d3a', 'X-Forwarded-For': '177.220.173.111, 130.176.160.132', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Accept-Language': ['pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,it;q=0.5,la;q=0.4,ru;q=0.3'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['BR'], 'content-type': ['application/json'], 'Host': ['ag40ai9r3i.execute-api.us-east-2.amazonaws.com'], 'origin': ['chrome-extension://biemppheiopfggogojnfpkngdkchelik'], 'sec-ch-ua': ['"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"macOS"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['none'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'], 'Via': ['2.0 9a0470365001a35d1ab4fa1b7a9f9daf.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['062XBuvUWRGcLRKCPHi85Xeguol6MCGvpUr6PMBmtvUk964lx9zv2A=='], 'X-Amzn-Trace-Id': ['Root=1-615a80b3-38d82b1d321a2bc35e373d3a'], 'X-Forwarded-For': ['177.220.173.111, 130.176.160.132'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': {'id': '2'}, 'stageVariables': None, 'requestContext': {'resourceId': 'ckny0h', 'resourcePath': '/service_areas/{id}', 'httpMethod': 'PUT', 'extendedRequestId': 'GqkMGE8SCYcF4RQ=', 'requestTime': '04/Oct/2021:04:18:59 +0000', 'path': '/dev/service_areas/2', 'accountId': '689726266135', 'protocol': 'HTTP/1.1', 'stage': 'dev', 'domainPrefix': 'ag40ai9r3i', 'requestTimeEpoch': 1633321139646, 'requestId': '29cb6f7a-61e2-4d2b-a7f3-5d9647ffa026', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '177.220.173.111', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 'user': None}, 'domainName': 'ag40ai9r3i.execute-api.us-east-2.amazonaws.com', 'apiId': 'ag40ai9r3i'}, 'body': '{\n    "price": 55.6\n}', 'isBase64Encoded': False}
handler(event, {})
