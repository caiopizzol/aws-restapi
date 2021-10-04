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
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Service area id {} successfully retrieved!'.format(service_area_id),
            'data': get_service_area(service_area_id)
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def get_service_area(service_area_id):
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
    WHERE providers_service_areas.id = %s;
    '''
    cur.execute(query, (service_area_id,))
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

# event = {
#     'id': 1
# }
# handler(event, {})
