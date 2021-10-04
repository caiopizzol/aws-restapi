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
    lat = event['queryStringParameters']['lat']
    lng = event['queryStringParameters']['lng']
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Service areas for coordinates: lat {} lng {}, were successfully retrieved!'.format(lat, lng),
            'data': get_service_area_within_coordinates(lat, lng)
        })        
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def get_service_area_within_coordinates(lat, lng):
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    SELECT
        json_build_object(
            'name', providers_service_areas.name,
            'price', providers_service_areas.price,
            'polygon', ST_AsGeoJSON(providers_service_areas.polygon),
            'provider_name', providers.name,
            'provider_email', providers.name,
            'provider_phone', providers.name,
            'proviver_language_name', languages.language,
            'proviver_language_code', languages.code,
            'proviver_currency_name', currencies.currency,
            'proviver_currency_code', currencies.code
        )
    FROM 
        providers_service_areas
    JOIN
        providers
        ON providers_service_areas.provider_id = providers.id
        JOIN 
            languages
            ON providers.language_id = languages.id
        JOIN
            currencies
            ON providers.currency_id = currencies.id
    WHERE ST_Intersects(
        polygon,
        ST_GeomFromText(
            'POINT(%s %s)',
            4326
            )
        );
    '''
    cur.execute(query,(
        float(lat),
        float(lng)
        )
    )
    result = cur.fetchall()      
    cur.close()
    if con is not None:
        con.close()
    return list(list(zip(*result))[0]) #Transforming from tuple to list

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con   

# event = {'resource': '/providers/{id}', 'path': '/providers/2', 'httpMethod': 'GET', 'headers': None, 'multiValueHeaders': None, 'queryStringParameters': {'lng': '-25.4084501', 'lat': '-49.2429226'}, 'multiValueQueryStringParameters': {'lng': ['-45.893'], 'lat': ['-29.478']}, 'pathParameters': {'id': '2'}, 'stageVariables': None, 'requestContext': {'resourceId': 'hjltou', 'resourcePath': '/providers/{id}', 'httpMethod': 'GET', 'extendedRequestId': 'GqZP1HFgCYcFegQ=', 'requestTime': '04/Oct/2021:03:04:17 +0000', 'path': '/providers/{id}', 'accountId': '689726266135', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1633316657944, 'requestId': '0fd5d91d-ef13-4070-b93f-eb273bd1097a', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws:iam::689726266135:user/caiopizzol', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.12.71 Linux/5.4.134-73.228.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard', 'accountId': '689726266135', 'caller': 'AIDA2BFXDTMLQEKORDNFA', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIA2BFXDTMLVZYJIZ4G', 'cognitoAuthenticationProvider': None, 'user': 'AIDA2BFXDTMLQEKORDNFA'}, 'domainName': 'testPrefix.testDomainName', 'apiId': 'ag40ai9r3i'}, 'body': None, 'isBase64Encoded': False}
# handler(event, {})
