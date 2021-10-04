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
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Provider id {} successfully retrieved!'.format(provider_id),
            'data': get_provider(provider_id)
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def get_provider(provider_id):
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    SELECT
        json_build_object(
            'name', providers.name,
            'email', providers.email,
            'phone', providers.phone,
            'language_code', languages.code,
            'language', languages.language,
            'currency_code', currencies.code,
            'currency', currencies.currency
        )
    FROM 
        providers
    JOIN 
        languages
        ON providers.language_id = languages.id
    JOIN
        currencies
        ON providers.currency_id = currencies.id
    WHERE providers.id = %s;
    '''
    cur.execute(query, (provider_id,))
    result = cur.fetchone()[0]
    cur.close()
    if con is not None:
        con.close()
    return result
    
def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con

# event = {'resource': '/providers/{id}', 'path': '/providers/2', 'httpMethod': 'GET', 'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,it;q=0.5,la;q=0.4,ru;q=0.3', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'BR', 'Host': 'ag40ai9r3i.execute-api.us-east-2.amazonaws.com', 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 'Via': '2.0 88ed6867c0889ee2caec1c3973510681.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'DSXFy0wsEJUsx7rFjwP4JXj_yWxHTW7Zi1lek93H4JkKixlVnXS09w==', 'X-Amzn-Trace-Id': 'Root=1-615a6b75-6be6368765928ebf7b13060e', 'X-Forwarded-For': '177.220.173.111, 130.176.160.169', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'], 'Accept-Encoding': ['gzip, deflate, br'], 'Accept-Language': ['pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,it;q=0.5,la;q=0.4,ru;q=0.3'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['BR'], 'Host': ['ag40ai9r3i.execute-api.us-east-2.amazonaws.com'], 'sec-ch-ua': ['"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"macOS"'], 'sec-fetch-dest': ['document'], 'sec-fetch-mode': ['navigate'], 'sec-fetch-site': ['none'], 'sec-fetch-user': ['?1'], 'upgrade-insecure-requests': ['1'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'], 'Via': ['2.0 88ed6867c0889ee2caec1c3973510681.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['DSXFy0wsEJUsx7rFjwP4JXj_yWxHTW7Zi1lek93H4JkKixlVnXS09w=='], 'X-Amzn-Trace-Id': ['Root=1-615a6b75-6be6368765928ebf7b13060e'], 'X-Forwarded-For': ['177.220.173.111, 130.176.160.169'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': {'id': '2'}, 'stageVariables': None, 'requestContext': {'resourceId': 'hjltou', 'resourcePath': '/providers/{id}', 'httpMethod': 'GET', 'extendedRequestId': 'GqW6ZFqtiYcFrxA=', 'requestTime': '04/Oct/2021:02:48:21 +0000', 'path': '/dev/providers/2', 'accountId': '689726266135', 'protocol': 'HTTP/1.1', 'stage': 'dev', 'domainPrefix': 'ag40ai9r3i', 'requestTimeEpoch': 1633315701596, 'requestId': 'eeee1db5-2b62-4174-a3f9-07c34593237d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '177.220.173.111', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36', 'user': None}, 'domainName': 'ag40ai9r3i.execute-api.us-east-2.amazonaws.com', 'apiId': 'ag40ai9r3i'}, 'body': None, 'isBase64Encoded': False}
# handler(event, {})
