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
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Service area list successfully retrieved!',
            'data': list_service_areas()
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def list_service_areas():
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
            'provider_language_name', languages.language,
            'provider_language_code', languages.code,
            'provider_currency_name', currencies.currency,
            'provider_currency_code', currencies.code
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
    '''
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    if con is not None:
        con.close()
    return list(list(zip(*result))[0])

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con  

# handler({}, {})
